output "instance_ip" {
  value       = aws_instance.pleiades.public_ip
  description = "Public IP of the EC2 instance"
}
output "instance_id" {
  value       = aws_instance.pleiades.id
  description = "EC2 instance ID"
}