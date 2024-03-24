provider "google" {
  credentials = file("parth-auth.json")
  project     = "csci-5409-cc-418214"
  region      = "northamerica-northeast1"
}

resource "google_container_cluster" "primary" {
  name     = "parth-cluster"
  location = "northamerica-northeast1-a"

  remove_default_node_pool = true
  initial_node_count = 1

  node_pool {
    name       = "primary-node-pool"
    node_count = 1

    node_config {
      machine_type = "e2-micro"
      disk_size_gb = 10
      disk_type    = "pd-standard"
      image_type   = "COS_CONTAINERD"

      oauth_scopes = [
        "https://www.googleapis.com/auth/cloud-platform"
      ]
    }
  }
}