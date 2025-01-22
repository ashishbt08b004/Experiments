```terraform
# Configure the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Create a variable for the number of EC2 instances
variable "num_instances" {
  type        = number
  default     = 5
  description = "Number of EC2 instances to create"
}

# Create a variable for the instance type
variable "instance_type" {
  type        = string
  default     = "c6g.xlarge"
  description = "Instance type to use"
}

# Create a variable for the root volume size
variable "root_volume_size" {
  type        = number
  default     = 30
  description = "Root volume size in GB"
}

# Create a variable for the number of RAM (in GB)
variable "ram" {
  type        = number
  default     = 16
  description = "Number of RAM in GB"
}

# Create a variable for the availability zone
variable "availability_zone" {
  type        = string
  default     = "us-west-2a"
  description = "Availability zone to use"
}

# Create the EC2 instances
resource "aws_instance" "example" {
  count         = var.num_instances
  ami           = "ami-abc123"
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.example.id]
  subnet_id              = aws_subnet.example.id

  # Create a block device for the root volume
  block_device {
    device_name = "/dev/sda1"
    delete_on_termination = true
    volume_size           = var.root_volume_size
  }

  # Add additional block devices with more RAM
  dynamic "block_device" {
    for_each = range(var.num_instances)
    content {
      device_name = "/dev/xvd${count.index}1"
      delete_on_termination = true
      volume_size           = (var.ram * var.num_instances) / count.index
    }
  }

  tags = {
    Name        = "EC2 instance ${count.index + 1}"
    Environment = "Dev"
  }
}

# Create a security group for the EC2 instances
resource "aws_security_group" "example" {
  name        = "ec2-sg"
  description = "Security group for EC2 instances"

  # Allow incoming traffic on port 22 (SSH)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outgoing traffic on any port
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create a subnet for the EC2 instances
resource "aws_subnet" "example" {
  name        = "subnet-ec2"
  description = "Subnet for EC2 instances"

  # Set up the subnet details
  cidr_block    = "10.0.1.0/24"
  availability_zone = var.availability_zone

  tags = {
    Name        = "Subnet"
    Environment = "Dev"
  }
}

# Output the public IP addresses of the EC2 instances
output "ec2_public_ips" {
  value       = aws_instance.example[*].public_ip
}
```

This Terraform script creates 5 EC2 machines with at least 16GB RAM in the most cost efficient manner on AWS. The instance type used is `c6g.xlarge`, which provides a good balance of performance and cost. The root volume size is set to 30 GB, and each additional block device has more RAM allocated to it. The script also creates a security group and subnet for the EC2 instances.

You can execute this script using the `terraform init` and `terraform apply` commands to create the EC2 instances on AWS. Make sure to replace the placeholder values with your actual AWS credentials and region.

Note: This script uses the Terraform 0.14 syntax, which is recommended for production environments. If you're using an earlier version of Terraform, please update to a supported version before running this script.