# Data Crawler

> [!Important]
> Docs is under construction 🚧

Crawler service for Exchange Rate App.

## Installation

### Pre-requisite

- [Python](https://www.python.org/downloads/) `v3.7` or latest
- [NodeJS](https://nodejs.org/en/download/) v18 or latest (optional, for deployment)

### Setup

1. Clone [this project](https://github.com/muhammadfajri-tif/exchange-rate-crawler).

    For example to clone using git with https:

    ```
    git clone https://github.com/muhammadfajri-tif/exchange-rate-crawler.git
    ```

2. Install required packages/dependencies

    > [!TIP]
    > Use virtual environments like venv to separate packages/dependencies that required for this project. To create virtual environments please refer to [this docs](https://docs.python.org/3/library/venv.html#creating-virtual-environments).


    ```bash
    pip install -r requirements.txt
    ```

3. Configure environments variable (`.env`)

    Copy the template from `.env.example`

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file by filling in the environment variables values. Each variable has its own purpose. Here's the available and required variables:

    | variable name | mandatory | description | 
    | --- | --- | --- |
    | `APP_NAME` | required | Stage name for the project. For example `local`, `dev` or `prod`. |
    | `BUCKET_NAME` | optional (used in production) | Name of AWS S3 bucket. Used for storing scraping data on the Cloud storage. Make sure the S3 bucket is already exist. |
    | `AWS_ACCESS_KEY` | required if `BUCKET_NAME` is set otherwise it's optional | Access key for grants programmatic access to AWS resources. Used to authenticate when uploading scraping data to S3. For information about AWS credentials, please refer to the [official docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions). |
    | `AWS_SECRET_ACCESS_KEY` | required if `BUCKET_NAME` is set otherwise it's optional | Secret access key is used in pairs with the access key for grants programmatic access to AWS resources. |
    | `AWS_REGION_NAME` | required if `BUCKET_NAME` is set otherwise it's optional | Used for set AWS Region that stores the S3 bucket. For example `us-east-1`, `ap-southeast-1`, etc. For information about AWS Regions, please refer to the [official docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html#Concepts.RegionsAndAvailabilityZones.Regions). |


## Deployment

### Run locally

coming soon...

### Run on AWS

coming soon...

## Troubleshooting

coming soon...
