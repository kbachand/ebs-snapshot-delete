import boto3
from pprint import pprint
#import sys
import argparse

ARG_HELP ="""
    --------------------------------------------------------------------------------
    Use to this EBS Snapshot Delete Script to delete snapshots that don't have a volume attached.

    Script Usage:
        python3 ebs-snapshot-delete.py (This is a dry run and will not delete any snapshots)
        python3 ebs-snapshot-delete.py --delete
        ** Without --delete appended to cli command this script will not delete snapshots **
    --------------------------------------------------------------------------------
    """
ec2_client = boto3.client('ec2')

# Empty list variable to store snapshots to delete with no volumes
snapshots_to_delete = list()

# Make a list of existing volumes
volume_response = ec2_client.describe_volumes()
volumes = [volume['VolumeId'] for volume in volume_response['Volumes']]

# Find snapshots without existing volume
snapshot_response = ec2_client.describe_snapshots(OwnerIds=['self'])

for snapshot in snapshot_response['Snapshots']:
    if snapshot['VolumeId'] not in volumes:
          snapshots_to_delete.append(snapshot['SnapshotId'])

pprint(snapshots_to_delete)
print("Total Snapshots with no volume:",len(snapshots_to_delete))

# Display profile and region infomation where data is being pulled from
session = boto3.Session()
print("Profile: ", session.profile_name)
print("Region: ", session.region_name)

# Deletion
total_errors = list()
total_deleted = list()

def delete(args):
    if args.delete is True and len(snapshots_to_delete) > 0:
        for snapshot_id in snapshots_to_delete:
            try:
                print("Deleting Snapshot with snapshot_id: " + snapshot_id)
                response = ec2_client.delete_snapshot(
                    SnapshotId=snapshot_id
                )
                total_deleted.append(snapshot_id)
            except Exception as e:
                total_errors.append(snapshot_id)
                print("Issue in deleting snapshot with id: " + snapshot_id + " error is: " + str(e))
        # Simple if statement to output total errors if any as well as total snapshots deleted
        if len(total_errors) > 0:
            print("Total Errors:", len(total_errors))
        else:
            print("There were no errors")

        print("Total Snapshots Deleted:", len(total_deleted))
    else:
        print("No snapshots deleted")

# Add functionality for cli argument to delete
if __name__ == '__main__':
    try:
        args = argparse.ArgumentParser(description=ARG_HELP, formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)
        args.add_argument('--delete','-d', dest='delete', action='store_true', help="Use to delete Volumes")
        args = args.parse_args()
        # Launch delete function
        delete(args)
    except KeyboardInterrupt:
        print("\n[!] Key Interrupt Detected...\n\n")
        exit(1)
    exit(0)
