# Operational Runbook for Global Data Analytics Pipeline

## Deployment

1. **Prerequisites**
   - Ensure that the environment variable `GITHUB_TOKEN` is set with the appropriate GitHub Access Token.
   - Verify that all necessary dependencies are installed.

2. **Deployment Steps**
   - Clone the repository:
     ```
     git clone https://github.com/heni1123/global-analytics-etl-pipeline.git
     cd global-analytics-etl-pipeline
     ```
   - Checkout the appropriate branch:
     ```
     git checkout main
     ```
   - Run the ETL pipeline:
     ```
     python -m etl_pipeline
     ```

3. **Post-Deployment Verification**
   - Check the logs to ensure that the ETL process completed successfully.
   - Validate that the data has been loaded into the `public.fact_crypto_markets` table.

## Monitoring

1. **Log Monitoring**
   - Monitor the ETL logs located in the `logs/` directory for any errors or warnings.
   - Use a log management tool to aggregate and analyze logs.

2. **Data Quality Checks**
   - Implement data quality checks to ensure that the data in `public.fact_crypto_markets` meets the expected standards.
   - Schedule regular audits of the data.

## Alerting

1. **Setup Alerts**
   - Configure alerts for failures in the ETL process using a monitoring tool (e.g., Prometheus, Grafana).
   - Set up email notifications for critical errors.

2. **Alert Criteria**
   - Alert on any ETL job failures.
   - Alert on data quality issues detected during monitoring.

## Rollback

1. **Rollback Procedure**
   - In case of a failure, revert to the last known good state of the `public.fact_crypto_markets` table.
   - Use the following SQL command to restore from a backup:
     ```
     DELETE FROM public.fact_crypto_markets;
     INSERT INTO public.fact_crypto_markets SELECT * FROM public.fact_crypto_markets_backup;
     ```

2. **Post-Rollback Verification**
   - Verify that the rollback was successful by checking the data integrity and consistency in the `public.fact_crypto_markets` table.
   - Review logs to identify the cause of the failure and address any issues before redeploying.