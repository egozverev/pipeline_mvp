from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform import hdx_adm0


def transform_adm0(country, config, **kwargs):
    print(f"COUNTRY v2.0: {country}")
    hdx_adm0.transform(source="cod",
                       input_filename="/opt/data/test/yem_adm_govyem_cso_ochayemen_20191002_GPKG.zip",
                       schema_filename="/usr/local/airflow/plugins/pipeline_plugin/schemas/admin0_affected_area_py.yml",
                       output_filename="/opt/data/test/yem_adm0_processed.zip",
                       country=country,
                       config=config)


class HDXAdm0Operator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            country: str,
            config,
            *args, **kwargs) -> None:
        self.country = country
        super().__init__(python_callable=transform_adm0, op_kwargs={"country": country, 'config': config}, *args,
                         **kwargs)