# ebs-snapshot-delete
A basic Python script that will list and delete EBS snapshots that are not attached or in-use in AWS.

## Setup
Follow the steps to get setup to use this script
* `git clone my-repo`
* `cd ebs-snapshot-delete`

## Script Usage
* `python3 ebs-snapshot-delete.py`  - Will display a list of snapshots to delete but will not delete any
* `python3 ebs-snapshot-delete.py --delete` - Deletes snapshots

## Requirements
* Python 3
* boto3
* awscli
