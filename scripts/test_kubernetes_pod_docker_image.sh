docker run -e FUNCTION_MODULE=pipeline_plugin.transform.hdx_adm0 \
           -e FUNCTION_NAME=transform \
           -e FUNCTION_ARGUMENTS="{\"country\":\"yemen\"}" \
           mapaction-task-image:latest