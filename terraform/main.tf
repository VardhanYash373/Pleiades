terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
provider "aws" {
  region = var.region
}
resource "aws_key_pair" "pleiades" {
  key_name   = "pleiades-key"
  public_key = file("~/.ssh/pleiades.pub")
}
resource "aws_security_group" "pleiades" {
  name        = "pleiades-sg"
  description = "SSH, k8s API and NodePorts"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }
  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }
  ingress {
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_instance" "pleiades" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = aws_key_pair.pleiades.key_name
  vpc_security_group_ids = [aws_security_group.pleiades.id]
  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }
  tags = {
    Name = "Pleiades"
  }
}
