import sys
import json

pre_upgrade_device_info_file = sys.argv[1]
with open(pre_upgrade_device_info_file) as f:
  pre_upgrade_device_info = json.load(f)

post_upgrade_device_info_file = sys.argv[2]
with open(post_upgrade_device_info_file) as f:
  post_upgrade_device_info = json.load(f)

results = {
  "_summary": {
    "pre_upgrade_device_info_file": pre_upgrade_device_info_file,
    "post_upgrade_device_info_file": post_upgrade_device_info_file
  }
}

# Compare virtual server
subset = "virtual_servers"
results[subset] = {}
for subset_pre in pre_upgrade_device_info[subset]:
  name = subset_pre["name"]
  results[subset][name] = {}

  subset_post = next(item for item in post_upgrade_device_info[subset] if item["name"] == name)

  for attr in [
    "enabled",
    "availability_status"
  ]:
    results[subset][name][attr] = "match" if subset_pre[attr] == subset_post[attr] else "mismatched"

# Compare LTM pool
subset = "ltm_pools"
results[subset] = {}
for subset_pre in pre_upgrade_device_info[subset]:
  name = subset_pre["name"]
  results[subset][name] = {}

  subset_post = next(item for item in post_upgrade_device_info[subset] if item["name"] == name)

  for attr in [
    "active_member_count",
    "availability_status"
  ]:
    results[subset][name][attr] = "match" if subset_pre[attr] == subset_post[attr] else "mismatched"


print(json.dumps(results, indent=2))
