"""TestS3BucketConnectorMethods
"""
import os
import unittest
import boto3
from moto import mock_s3

from xetra.common.s3 import S3BucketConnector



class TestS3BucketConnectorMethods(unittest.TestCase):
    """Testing the S3 Bucket Connector class

    Args:
        unittest (_type_): _description_
    """

    def setup(self):
        """Setting up the environment
        """
        # mocking s3 connection start
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        # defining the class arguments-
        self.s3_access_key ='AWS_SECRET_ACCESS_ID'
        self.s3_secret_key = 'AWS_SECRET_ACCESS_KEY'
        self.s3_endpoint_url ='https://s3.eu-central-1.amazonaws.com'
        self.s3_bucket_name = 'test_bucket'
        # creating s3 access keys and environment 
        os.environ[self.s3_access_key] = 'KEY1'
        os.environ[self.s3_secret_key] = 'KEY2'
        # creaing a a bucket on the mocked s3
        self.s3 = boto3.resource(service_name='s3', endpoint_url=self.endpoint_url)
        self.s3.create_bucket(Bucket=self.s3_bucket_name, 
        CreatedBucketConfiguration = {
            'LocationConfiguration: eu-central-1'
        })
        self.s3_bucket = self.s3.Bucket(self.s3_bucket_name)
        # creating a testing instance
        self.s3_bucket_conn = S3BucketConnector(self.s3_access_key, self.s3_secret_key, self.s3_endpoint_url, self.s3_bucket_name )


    def tearDown(self):
        """Executing after unittest"""
        # mocking s3 connection stop
        self.mock_s3.stop()

    def test_list_files_in_prefix_ok(self):
        """Tests the list_files_in_prefix method for getting 2 file keys
            as list on the mocked s3 bucket.
        """
        # Expected result
        prefix_exp = 'prefix/'
        key1_exp = f'{prefix_exp}test1.csv'
        key2_exp = f'{prefix_exp}test2.csv'
        # Test unit
        csv_content = """col1,col2
        valA,valB
        """
        self.s3_bucket.put_object(Body=csv_content, key=key1_exp)
        self.s3_bucket.put_object(Body=csv_content, key=key2_exp)
        # Methods execution
        list_result = self.s3_bucket_conn.list_files_in_prefix(prefix_exp)
        # test/s after method execution
        self.assertEqual(len(list_result), 2)
        self.assertEqual(key1_exp, list_result)
        self.assertEqual(key2_exp, list_result) 
        # Cleanup after test
        self.s3_bucket.delete_objects(
            Delete={
                'Objects': [
                    {'Key': key1_exp},
                    {'Key': key2_exp}
                ]
            }
        )

    def test_list_files_in_wrong_prefix(self):
        """
        Test the list_files_in_prefix method in case of wrong / not-existing prefix
        """
        # Expected result
        prefix_exp = 'no-prefix/'
        # Methods execution
        list_result = self.s3_bucket_conn.list_files_in_prefix(prefix_exp)
        # test/s after method execution
        self.assertTrue(not list_result)


 

if __name__ == '__main__':
    unittest.main
    ## Manual testing
    # testIns = TestS3BucketConnectorMethods()
    # testIns.setup()
    # testIns.test_list_files_in_prefix_ok()
    # testIns.tearDown()