terraform { required_version = ">= 1.6" }
variable "requests_per_second" {
  type = number
  default = 101
  validation {
    condition = var.requests_per_second >= 0
    error_message = "Requests per second must be nonnegative."
  }
}
variable "per_instance_capacity" {
  type = number
  default = 100
  validation {
    condition = var.per_instance_capacity > 0
    error_message = "Capacity must be positive."
  }
}
variable "target_utilization" {
  type = number
  default = 0.5
  validation {
    condition = var.target_utilization > 0 && var.target_utilization <= 1
    error_message = "Utilization must be greater than zero and at most one."
  }
}
output "modeled_instance_count" { value = max(1, ceil(var.requests_per_second / (var.per_instance_capacity * var.target_utilization))) }
