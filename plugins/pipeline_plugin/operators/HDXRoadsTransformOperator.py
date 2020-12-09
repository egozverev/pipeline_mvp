from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform.hdx_road import transform


class HDXRoadsTransformOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            country: str,
            config,
            *args, **kwargs) -> None:
        self.country = country
        super().__init__(python_callable=self.transform_roads, op_kwargs={"country": country, 'config': config}, *args,
                         **kwargs)

    def transform_roads(self, country, config, **kwargs):
        print(f"COUNTRY v2.0: {country}")
        transform(input_filename="/opt/data/test/ymn-roads.zip",
                  schema_filename="/usr/local/airflow/plugins/pipeline_plugin/schemas/roads_affected_area_py.yml",
                  output_filename="/opt/data/test/yem_tran_rds_ln_s1_ocha_pp.shp",
                  config=config)
