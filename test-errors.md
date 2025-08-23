🔮 Running test suite
============================================= test session starts =============================================
platform linux -- Python 3.12.3, pytest-8.4.1, pluggy-1.6.0 -- /home/cezar/automagik/automagik-spark/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/cezar/automagik/automagik-spark
configfile: pytest.ini
plugins: anyio-4.9.0, mock-3.14.1, asyncio-1.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=session, asyncio_default_test_loop_scope=function
collected 152 items                                                                                           

tests/api/test_api.py::test_root_endpoint PASSED                                                        [  0%]
tests/api/test_api.py::test_docs_endpoint PASSED                                                        [  1%]
tests/api/test_api.py::test_openapi_json_endpoint PASSED                                                [  1%]
tests/api/test_api.py::test_redoc_endpoint PASSED                                                       [  2%]
tests/api/test_api.py::test_cors_configuration_default PASSED                                           [  3%]
tests/api/test_api.py::test_cors_configuration_custom PASSED                                            [  3%]
tests/api/test_api.py::test_cors_configuration_invalid_origin PASSED                                    [  4%]
tests/api/test_api.py::test_health_check PASSED                                                         [  5%]
tests/api/test_auth.py::test_api_no_key_configured PASSED                                               [  5%]
tests/api/test_auth.py::test_api_key_required PASSED                                                    [  6%]
tests/api/test_auth.py::test_api_key_valid PASSED                                                       [  7%]
tests/api/test_auth.py::test_api_key_invalid PASSED                                                     [  7%]
tests/api/test_auth.py::test_verify_api_key_no_key_configured PASSED                                    [  8%]
tests/api/test_auth.py::test_verify_api_key_with_key_configured PASSED                                  [  9%]
tests/api/test_auth.py::test_api_key_case_sensitive PASSED                                              [  9%]
tests/api/test_auth.py::test_api_key_whitespace PASSED                                                  [ 10%]
tests/api/test_config.py::test_get_cors_origins_default PASSED                                          [ 11%]
tests/api/test_config.py::test_get_cors_origins_custom PASSED                                           [ 11%]
tests/api/test_config.py::test_get_cors_origins_empty PASSED                                            [ 12%]
tests/api/test_config.py::test_get_api_host_default PASSED                                              [ 13%]
tests/api/test_config.py::test_get_api_host_custom PASSED                                               [ 13%]
tests/api/test_config.py::test_get_api_port_default PASSED                                              [ 14%]
tests/api/test_config.py::test_get_api_port_custom PASSED                                               [ 15%]
tests/api/test_config.py::test_get_api_port_invalid PASSED                                              [ 15%]
tests/api/test_config.py::test_get_api_key_default PASSED                                               [ 16%]
tests/api/test_config.py::test_get_api_key_custom PASSED                                                [ 17%]
tests/api/test_config.py::test_get_langflow_api_url_default PASSED                                      [ 17%]
tests/api/test_config.py::test_get_langflow_api_url_custom PASSED                                       [ 18%]
tests/api/test_config.py::test_get_langflow_api_key_default PASSED                                      [ 19%]
tests/api/test_config.py::test_get_langflow_api_key_custom PASSED                                       [ 19%]
tests/api/test_sources.py::TestSourcesCreate::test_create_langflow_source_success FAILED                [ 20%]
tests/api/test_sources.py::TestSourcesCreate::test_create_automagik_agents_source_success FAILED        [ 21%]
tests/api/test_sources.py::TestSourcesCreate::test_create_automagik_hive_source_success FAILED          [ 21%]
tests/api/test_sources.py::TestSourcesCreate::test_create_source_duplicate_url ERROR                    [ 22%]
tests/api/test_sources.py::TestSourcesCreate::test_create_source_invalid_url PASSED                     [ 23%]
tests/api/test_sources.py::TestSourcesCreate::test_create_source_health_check_fails FAILED              [ 23%]
tests/api/test_sources.py::TestSourcesCreate::test_create_source_unauthorized PASSED                    [ 24%]
tests/api/test_sources.py::TestSourcesCreate::test_create_source_empty_api_key FAILED                   [ 25%]
tests/api/test_sources.py::TestSourcesList::test_list_sources_success ERROR                             [ 25%]
tests/api/test_sources.py::TestSourcesList::test_list_sources_with_status_filter ERROR                  [ 26%]
tests/api/test_sources.py::TestSourcesList::test_list_sources_unauthorized PASSED                       [ 26%]
tests/api/test_sources.py::TestSourcesGet::test_get_source_success ERROR                                [ 27%]
tests/api/test_sources.py::TestSourcesGet::test_get_source_not_found FAILED                             [ 28%]
tests/api/test_sources.py::TestSourcesGet::test_get_source_invalid_id PASSED                            [ 28%]
tests/api/test_sources.py::TestSourcesGet::test_get_source_unauthorized ERROR                           [ 29%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_name ERROR                             [ 30%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_url ERROR                              [ 30%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_api_key ERROR                          [ 31%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_status ERROR                           [ 32%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_type ERROR                             [ 32%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_url_conflict ERROR                     [ 33%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_not_found FAILED                       [ 34%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_unauthorized ERROR                     [ 34%]
tests/api/test_sources.py::TestSourcesUpdate::test_update_source_multiple_fields ERROR                  [ 35%]
tests/api/test_sources.py::TestSourcesDelete::test_delete_source_success ERROR                          [ 36%]
tests/api/test_sources.py::TestSourcesDelete::test_delete_source_not_found FAILED                       [ 36%]
tests/api/test_sources.py::TestSourcesDelete::test_delete_source_unauthorized ERROR                     [ 37%]
tests/api/test_sources.py::TestSourceValidation::test_wrong_health_status FAILED                        [ 38%]
tests/api/test_sources.py::TestSourceValidation::test_automagik_hive_fallback_status FAILED             [ 38%]
tests/api/test_sources.py::TestEncryption::test_api_key_encryption FAILED                               [ 39%]
tests/api/test_sources.py::TestEncryption::test_encryption_key_from_environment PASSED                  [ 40%]
tests/api/test_sources.py::TestURLHandling::test_url_trailing_slash_removed FAILED                      [ 40%]
tests/api/test_sources.py::TestURLHandling::test_url_validation_with_ports FAILED                       [ 41%]
tests/api/test_sources.py::TestErrorHandling::test_network_timeout FAILED                               [ 42%]
tests/api/test_sources.py::TestErrorHandling::test_invalid_json_response FAILED                         [ 42%]
tests/api/test_sources.py::TestErrorHandling::test_missing_required_fields PASSED                       [ 43%]
tests/api/test_sources.py::TestErrorHandling::test_invalid_source_type PASSED                           [ 44%]
tests/api/test_sources.py::TestErrorHandling::test_invalid_uuid_format FAILED                           [ 44%]
tests/core/database/test_database_init.py::test_database_tables_exist PASSED                            [ 45%]
tests/core/scheduler/test_scheduler_manager.py::test_create_schedule_with_valid_interval PASSED         [ 46%]
tests/core/scheduler/test_scheduler_manager.py::test_create_schedule_with_valid_cron PASSED             [ 46%]
tests/core/scheduler/test_scheduler_manager.py::test_create_schedule_with_invalid_interval PASSED       [ 47%]
tests/core/scheduler/test_scheduler_manager.py::test_create_schedule_with_invalid_cron PASSED           [ 48%]
tests/core/scheduler/test_scheduler_manager.py::test_create_schedule_with_nonexistent_workflow PASSED   [ 48%]
tests/core/scheduler/test_scheduler_manager.py::test_create_schedule_with_invalid_interval_formats PASSED [ 49%]
tests/core/scheduler/test_scheduler_manager.py::test_create_schedule_with_valid_interval_formats PASSED [ 50%]
tests/core/scheduler/test_scheduler_manager.py::test_update_schedule_status PASSED                      [ 50%]
tests/core/scheduler/test_scheduler_manager.py::test_update_schedule_status_invalid_action PASSED       [ 51%]
tests/core/scheduler/test_scheduler_manager.py::test_update_schedule_status_nonexistent_schedule PASSED [ 51%]
tests/core/scheduler/test_scheduler_manager.py::test_list_schedules PASSED                              [ 52%]
tests/core/scheduler/test_scheduler_manager.py::test_delete_schedule PASSED                             [ 53%]
tests/core/scheduler/test_scheduler_manager.py::test_delete_nonexistent_schedule PASSED                 [ 53%]
tests/core/workflows/components/test_components.py::test_get_flow_components PASSED                     [ 54%]
tests/core/workflows/scheduling/test_scheduling.py::test_create_schedule PASSED                         [ 55%]
tests/core/workflows/scheduling/test_scheduling.py::test_delete_schedule PASSED                         [ 55%]
tests/core/workflows/scheduling/test_scheduling.py::test_delete_nonexistent_schedule PASSED             [ 56%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_manager_initialization PASSED [ 57%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_validate_success PASSED     [ 57%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_validate_health_failure PASSED [ 58%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_list_agents PASSED          [ 59%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_list_teams PASSED           [ 59%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_list_workflows PASSED       [ 60%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_list_flows_combined PASSED  [ 61%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_get_flow_agent PASSED       [ 61%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_get_flow_not_found PASSED   [ 62%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_run_agent FAILED            [ 63%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_run_team PASSED             [ 63%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_run_workflow PASSED         [ 64%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_run_flow_not_found PASSED   [ 65%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_sync_list_flows PASSED      [ 65%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_sync_get_flow PASSED        [ 66%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_sync_run_agent FAILED       [ 67%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_context_managers PASSED     [ 67%]
tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_async_context_manager PASSED [ 68%]
tests/core/workflows/test_automagik_hive.py::TestSourceTypeEnum::test_automagik_hive_exists PASSED      [ 69%]
tests/core/workflows/test_automagik_hive.py::TestSourceTypeEnum::test_all_source_types PASSED           [ 69%]
tests/core/workflows/test_delete_flow.py::test_delete_workflow_with_full_uuid PASSED                    [ 70%]
tests/core/workflows/test_delete_flow.py::test_delete_workflow_with_truncated_uuid PASSED               [ 71%]
tests/core/workflows/test_delete_flow.py::test_delete_workflow_with_related_objects PASSED              [ 71%]
tests/core/workflows/test_delete_flow.py::test_delete_workflow_with_task_logs PASSED                    [ 72%]
tests/core/workflows/test_delete_flow.py::test_delete_nonexistent_workflow PASSED                       [ 73%]
tests/core/workflows/test_delete_flow.py::test_delete_workflow_invalid_uuid PASSED                      [ 73%]
tests/core/workflows/test_flow_analyzer.py::test_analyze_component_with_tweakable_params PASSED         [ 74%]
tests/core/workflows/test_flow_analyzer.py::test_analyze_component_empty_node PASSED                    [ 75%]
tests/core/workflows/test_flow_analyzer.py::test_get_flow_components PASSED                             [ 75%]
tests/core/workflows/test_flow_analyzer.py::test_get_flow_components_empty_flow PASSED                  [ 76%]
tests/core/workflows/test_flow_analyzer.py::test_get_flow_components_missing_fields PASSED              [ 76%]
tests/core/workflows/test_flow_execution.py::test_successful_flow_execution PASSED                      [ 77%]
tests/core/workflows/test_flow_execution.py::test_failed_flow_execution PASSED                          [ 78%]
tests/core/workflows/test_flow_execution.py::test_input_value_handling PASSED                           [ 78%]
tests/core/workflows/test_flow_execution.py::test_network_error_handling PASSED                         [ 79%]
tests/core/workflows/test_flow_execution.py::test_invalid_input_data PASSED                             [ 80%]
tests/core/workflows/test_flow_execution.py::test_timeout_handling PASSED                               [ 80%]
tests/core/workflows/test_flow_execution.py::test_missing_components PASSED                             [ 81%]
tests/core/workflows/test_flow_execution.py::test_malformed_response PASSED                             [ 82%]
tests/core/workflows/test_flow_execution.py::test_client_close PASSED                                   [ 82%]
tests/core/workflows/test_flow_execution.py::test_error_logging_with_traceback PASSED                   [ 83%]
tests/core/workflows/test_flow_execution.py::test_api_key_handling PASSED                               [ 84%]
tests/core/workflows/test_flow_execution.py::test_input_data_formats PASSED                             [ 84%]
tests/core/workflows/test_flow_execution.py::test_manager_initialization PASSED                         [ 85%]
tests/core/workflows/test_flow_execution.py::test_manager_not_initialized_error PASSED                  [ 86%]
tests/core/workflows/test_local_workflow.py::test_get_workflow_by_id PASSED                             [ 86%]
tests/core/workflows/test_local_workflow.py::test_get_nonexistent_workflow PASSED                       [ 87%]
tests/core/workflows/test_local_workflow.py::test_list_workflows PASSED                                 [ 88%]
tests/core/workflows/test_local_workflow.py::test_delete_workflow_by_id PASSED                          [ 88%]
tests/core/workflows/test_local_workflow.py::test_delete_workflow_by_partial_id PASSED                  [ 89%]
tests/core/workflows/test_local_workflow.py::test_delete_nonexistent_workflow PASSED                    [ 90%]
tests/core/workflows/test_local_workflow_manager.py::test_get_workflow_by_id PASSED                     [ 90%]
tests/core/workflows/test_local_workflow_manager.py::test_get_workflow_by_remote_id PASSED              [ 91%]
tests/core/workflows/test_local_workflow_manager.py::test_list_workflows PASSED                         [ 92%]
tests/core/workflows/test_local_workflow_manager.py::test_delete_workflow_by_id PASSED                  [ 92%]
tests/core/workflows/test_local_workflow_manager.py::test_delete_workflow_by_prefix PASSED              [ 93%]
tests/core/workflows/test_local_workflow_manager.py::test_delete_workflow_failure PASSED                [ 94%]
tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_get_source_manager_hive PASSED [ 94%]
tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_list_remote_flows_hive FAILED [ 95%]
tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_get_remote_flow_hive FAILED [ 96%]
tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_sync_flow_hive FAILED [ 96%]
tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_unsupported_source_type_error PASSED [ 97%]
tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_source_type_enum_values PASSED [ 98%]
tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_hive_source_handles_empty_flows FAILED [ 98%]
tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_hive_source_connection_error FAILED [ 99%]
tests/integration/flows/test_remote_flows.py::test_remote_api_error_handling SKIPPED (LangFlow API
configuration (URL and API key) not found)                                                              [100%]

=================================================== ERRORS ====================================================
____________________ ERROR at setup of TestSourcesCreate.test_create_source_duplicate_url _____________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_________________________ ERROR at setup of TestSourcesList.test_list_sources_success _________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
___________________ ERROR at setup of TestSourcesList.test_list_sources_with_status_filter ____________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
__________________________ ERROR at setup of TestSourcesGet.test_get_source_success ___________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
________________________ ERROR at setup of TestSourcesGet.test_get_source_unauthorized ________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_________________________ ERROR at setup of TestSourcesUpdate.test_update_source_name _________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_________________________ ERROR at setup of TestSourcesUpdate.test_update_source_url __________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_______________________ ERROR at setup of TestSourcesUpdate.test_update_source_api_key ________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
________________________ ERROR at setup of TestSourcesUpdate.test_update_source_status ________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_________________________ ERROR at setup of TestSourcesUpdate.test_update_source_type _________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_____________________ ERROR at setup of TestSourcesUpdate.test_update_source_url_conflict _____________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_____________________ ERROR at setup of TestSourcesUpdate.test_update_source_unauthorized _____________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
___________________ ERROR at setup of TestSourcesUpdate.test_update_source_multiple_fields ____________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_______________________ ERROR at setup of TestSourcesDelete.test_delete_source_success ________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_____________________ ERROR at setup of TestSourcesDelete.test_delete_source_unauthorized _____________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:121: in created_source
    response = client.post("/api/v1/sources/", json=sample_source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
================================================== FAILURES ===================================================
____________________________ TestSourcesCreate.test_create_langflow_source_success ____________________________
tests/api/test_sources.py:155: in test_create_langflow_source_success
    assert response.status_code == 201
E   assert 400 == 201
E    +  where 400 = <Response [400 Bad Request]>.status_code
________________________ TestSourcesCreate.test_create_automagik_agents_source_success ________________________
tests/api/test_sources.py:192: in test_create_automagik_agents_source_success
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2354: in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:794: in _handle_exception
    raise error
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:375: in query
    ???
E   RuntimeError: Task <Task pending name='anyio.from_thread.BlockingPortal._call_func' coro=<BlockingPortal._call_func() running at /home/cezar/automagik/automagik-spark/.venv/lib/python3.12/site-packages/anyio/from_thread.py:221> cb=[TaskGroup._spawn.<locals>.task_done() at /home/cezar/automagik/automagik-spark/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:794]> got Future <Future pending cb=[BaseProtocol._on_waiter_completed()]> attached to a different loop
_________________________ TestSourcesCreate.test_create_automagik_hive_source_success _________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:226: in test_create_automagik_hive_source_success
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:9000',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
___________________________ TestSourcesCreate.test_create_source_health_check_fails ___________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:279: in test_create_source_health_check_fails
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:9999',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_____________________________ TestSourcesCreate.test_create_source_empty_api_key ______________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:321: in test_create_source_empty_api_key
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
__________________________________ TestSourcesGet.test_get_source_not_found ___________________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:380: in test_get_source_not_found
    response = client.get(f"/api/v1/sources/{fake_id}", headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:465: in get
    return super().get(
.venv/lib/python3.12/site-packages/httpx/_client.py:1053: in get
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:179: in get_source
    source = await session.get(WorkflowSource, source_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:606: in get
    return await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:3694: in get
    return self._get_impl(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:3873: in _get_impl
    return db_load_fn(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/loading.py:694: in load_on_pk_identity
    session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id AS workflow_sources_id, workflow_sources.name AS workflow_sources_name, workflow_sources.source_type AS workflow_sources_source_type, workflow_sources.url AS workflow_sources_url, workflow_sources.encrypted_api_key AS workflow_sources_encrypted_api_key, workflow_sources.version_info AS workflow_sources_version_info, workflow_sources.status AS workflow_sources_status, workflow_sources.created_at AS workflow_sources_created_at, workflow_sources.updated_at AS workflow_sources_updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.id = $1::UUID]
E   [parameters: (UUID('7811b7ad-9eee-451b-aacd-c86e4fa3ffe0'),)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_______________________________ TestSourcesUpdate.test_update_source_not_found ________________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:552: in test_update_source_not_found
    response = client.patch(
.venv/lib/python3.12/site-packages/starlette/testclient.py:600: in patch
    return super().patch(
.venv/lib/python3.12/site-packages/httpx/_client.py:1218: in patch
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:192: in update_source
    source = await session.get(WorkflowSource, source_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:606: in get
    return await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:3694: in get
    return self._get_impl(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:3873: in _get_impl
    return db_load_fn(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/loading.py:694: in load_on_pk_identity
    session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id AS workflow_sources_id, workflow_sources.name AS workflow_sources_name, workflow_sources.source_type AS workflow_sources_source_type, workflow_sources.url AS workflow_sources_url, workflow_sources.encrypted_api_key AS workflow_sources_encrypted_api_key, workflow_sources.version_info AS workflow_sources_version_info, workflow_sources.status AS workflow_sources_status, workflow_sources.created_at AS workflow_sources_created_at, workflow_sources.updated_at AS workflow_sources_updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.id = $1::UUID]
E   [parameters: (UUID('9753a39d-0bcc-4f3b-8abf-52388ae1ba4f'),)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_______________________________ TestSourcesDelete.test_delete_source_not_found ________________________________
tests/api/test_sources.py:633: in test_delete_source_not_found
    assert response.status_code == 404
E   assert 400 == 404
E    +  where 400 = <Response [400 Bad Request]>.status_code
________________________________ TestSourceValidation.test_wrong_health_status ________________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:665: in test_wrong_health_status
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
__________________________ TestSourceValidation.test_automagik_hive_fallback_status ___________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:696: in test_automagik_hive_fallback_status
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:9000',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
___________________________________ TestEncryption.test_api_key_encryption ____________________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:730: in test_api_key_encryption
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_______________________________ TestURLHandling.test_url_trailing_slash_removed _______________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:780: in test_url_trailing_slash_removed
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_______________________________ TestURLHandling.test_url_validation_with_ports ________________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:816: in test_url_validation_with_ports
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
___________________________________ TestErrorHandling.test_network_timeout ____________________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:840: in test_network_timeout
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
________________________________ TestErrorHandling.test_invalid_json_response _________________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:863: in test_invalid_json_response
    response = client.post("/api/v1/sources/", json=source_data, headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:538: in post
    return super().post(
.venv/lib/python3.12/site-packages/httpx/_client.py:1144: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:123: in create_source
    result = await session.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources 
E   WHERE workflow_sources.url = $1::VARCHAR]
E   [parameters: ('http://localhost:7860',)]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
_________________________________ TestErrorHandling.test_invalid_uuid_format __________________________________
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:843: in _start_transaction
    await self._transaction.start()
.venv/lib/python3.12/site-packages/asyncpg/transaction.py:146: in start
    await self._connection.execute(query)
.venv/lib/python3.12/site-packages/asyncpg/connection.py:349: in execute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:360: in query
    ???
asyncpg/protocol/protocol.pyx:745: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests/api/test_sources.py:906: in test_invalid_uuid_format
    response = client.get(f"/api/v1/sources/{invalid_id}", headers=auth_headers)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:465: in get
    return super().get(
.venv/lib/python3.12/site-packages/httpx/_client.py:1053: in get
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:437: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
.venv/lib/python3.12/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
.venv/lib/python3.12/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
.venv/lib/python3.12/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
.venv/lib/python3.12/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:456: in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
/usr/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
.venv/lib/python3.12/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
             ^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
.venv/lib/python3.12/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
.venv/lib/python3.12/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
.venv/lib/python3.12/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
.venv/lib/python3.12/site-packages/starlette/routing.py:73: in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
.venv/lib/python3.12/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
automagik_spark/api/routers/sources.py:168: in list_sources
    result = await session.execute(query)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py:463: in execute
    result = await greenlet_spawn(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2365: in execute
    return self._execute_internal(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2251: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
.venv/lib/python3.12/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1415: in execute
    return meth(
.venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py:523: in _execute_on_connection
    return connection._execute_clauseelement(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1637: in _execute_clauseelement
    ret = self._execute_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1842: in _execute_context
    return self._exec_single_context(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1982: in _exec_single_context
    self._handle_dbapi_exception(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2351: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1963: in _exec_single_context
    self.dialect.do_execute(
.venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py:943: in do_execute
    cursor.execute(statement, parameters)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:580: in execute
    self._adapt_connection.await_(
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:515: in _prepare_and_execute
    await adapt_connection._start_transaction()
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:845: in _start_transaction
    self._handle_exception(error)
.venv/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:792: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
E   FROM workflow_sources]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
___________________________________ TestAutomagikHiveManager.test_run_agent ___________________________________
tests/core/workflows/test_automagik_hive.py:295: in test_run_agent
    assert result['result'] == 'Agent response'
E   assert "{'response': {'content': 'Agent response'}, 'session_id': 'session123', 'run_id': 'run456', 'agent_id': 'test-agent', 'status': 'completed'}" == 'Agent response'
E     
E     - Agent response
E     + {'response': {'content': 'Agent response'}, 'session_id': 'session123', 'run_id': 'run456', 'agent_id': 'test-agent', 'status': 'completed'}
________________________________ TestAutomagikHiveManager.test_sync_run_agent _________________________________
tests/core/workflows/test_automagik_hive.py:443: in test_sync_run_agent
    assert result['result'] == 'Agent response'
E   assert "{'response': {'content': 'Agent response'}, 'session_id': 'session123', 'status': 'completed'}" == 'Agent response'
E     
E     - Agent response
E     + {'response': {'content': 'Agent response'}, 'session_id': 'session123', 'status': 'completed'}
_______________________ TestWorkflowManagerHiveIntegration.test_list_remote_flows_hive ________________________
tests/core/workflows/test_manager_hive_integration.py:99: in test_list_remote_flows_hive
    assert len(flows) == 3
E   AssertionError: assert 9 == 3
E    +  where 9 = len([{'id': 'genie-debug', 'name': '\U0001f50d Genie Debug', 'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue investigation,  root cause analysis, and problem resolution. Equipped with comprehensive  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-dev', 'name': '\U0001f9de Genie Dev - Development Domain Coordinator', 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-quality', 'name': '\U0001f527 Genie Quality - Code Quality Domain Coordinator', 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-testing', 'name': '\U0001f9ea Genie Testing - Testing Domain Coordinator', 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'master-genie', 'name': '\U0001f9de Master Genie - Ultimate Development Companion', 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-agent', 'name': '\U0001f527 Template Agent', 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-team', 'name': 'Template Team', 'description': 'Template demonstrating all Agno Team parameters', 'data': {'type': 'hive_team', 'mode': 'route', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'template-agent', 'name': '\U0001f527 Template Agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_template-team', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 1}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '\U0001f465', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie', 'name': '\U0001f9de Genie', 'description': '**GENIE ARCHITECTURE** \U0001f916\u2728  Clean, efficient coordination through 3 domain specialists + Master Genie dual identity. Strategic orchestration commanding specialized coordinators through intelligent delegation. NEVER codes directly - maintains strategic focus through obsessive perfectionism.\n', 'data': {'type': 'hive_team', 'mode': 'coordinate', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'genie-dev', 'name': '\U0001f9de Genie Dev - Development Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'instructions': None}, {'agent_id': 'genie-testing', 'name': '\U0001f9ea Genie Testing - Testing Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'instructions': None}, {'agent_id': 'genie-quality', 'name': '\U0001f527 Genie Quality - Code Quality Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'instructions': None}, {'agent_id': 'master-genie', 'name': '\U0001f9de Master Genie - Ultimate Development Companion', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_genie', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 4}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '\U0001f465', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features', 'data': {'type': 'hive_workflow', 'steps': [], 'workflow_data': {'workflow_id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features'}}, 'is_component': False, 'folder_id': None, 'folder_name': 'Workflows', 'icon': '\u26a1', 'icon_bg_color': '#DC2626', 'liked': False, 'tags': ['workflow', 'multi-step', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}])
________________________ TestWorkflowManagerHiveIntegration.test_get_remote_flow_hive _________________________
tests/core/workflows/test_manager_hive_integration.py:128: in test_get_remote_flow_hive
    assert flow is not None
E   assert None is not None
---------------------------------------------- Captured log call ----------------------------------------------
WARNING  automagik_spark.core.workflows.manager:manager.py:183 Unsupported source type
___________________________ TestWorkflowManagerHiveIntegration.test_sync_flow_hive ____________________________
tests/core/workflows/test_manager_hive_integration.py:155: in test_sync_flow_hive
    result = await workflow_manager.sync_flow(
automagik_spark/core/workflows/manager.py:306: in sync_flow
    raise ValueError(f"No source found containing flow {flow_id}")
E   ValueError: No source found containing flow master-genie
___________________ TestWorkflowManagerHiveIntegration.test_hive_source_handles_empty_flows ___________________
tests/core/workflows/test_manager_hive_integration.py:207: in test_hive_source_handles_empty_flows
    assert flows == []
E   AssertionError: assert [{'id': 'genie-debug', 'name': '🔍 Genie Debug', 'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue investigation,  root cause analysis, and problem resolution. Equipped with comprehensive  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-dev', 'name': '🧞 Genie Dev - Development Domain Coordinator', 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-quality', 'name': '🔧 Genie Quality - Code Quality Domain Coordinator', 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-testing', 'name': '🧪 Genie Testing - Testing Domain Coordinator', 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'master-genie', 'name': '🧞 Master Genie - Ultimate Development Companion', 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-agent', 'name': '🔧 Template Agent', 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-team', 'name': 'Template Team', 'description': 'Template demonstrating all Agno Team parameters', 'data': {'type': 'hive_team', 'mode': 'route', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'template-agent', 'name': '🔧 Template Agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_template-team', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 1}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '👥', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie', 'name': '🧞 Genie', 'description': '**GENIE ARCHITECTURE** 🤖✨  Clean, efficient coordination through 3 domain specialists + Master Genie dual identity. Strategic orchestration commanding specialized coordinators through intelligent delegation. NEVER codes directly - maintains strategic focus through obsessive perfectionism.\n', 'data': {'type': 'hive_team', 'mode': 'coordinate', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'genie-dev', 'name': '🧞 Genie Dev - Development Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'instructions': None}, {'agent_id': 'genie-testing', 'name': '🧪 Genie Testing - Testing Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'instructions': None}, {'agent_id': 'genie-quality', 'name': '🔧 Genie Quality - Code Quality Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'instructions': None}, {'agent_id': 'master-genie', 'name': '🧞 Master Genie - Ultimate Development Companion', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_genie', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 4}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '👥', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features', 'data': {'type': 'hive_workflow', 'steps': [], 'workflow_data': {'workflow_id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features'}}, 'is_component': False, 'folder_id': None, 'folder_name': 'Workflows', 'icon': '⚡', 'icon_bg_color': '#DC2626', 'liked': False, 'tags': ['workflow', 'multi-step', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}] == []
E     
E     Left contains 9 more items, first extra item: {'created_at': None, 'data': {'add_context': True, 'instructions': None, 'memory': None, 'model': {'model': 'gpt-4o', ...  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'folder_id': None, ...}
E     
E     Full diff:
E     - []
E     + [
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue '
E     +         'investigation,  root cause analysis, and problem resolution. Equipped '
E     +         'with comprehensive  debugging tools including database queries, '
E     +         'system analysis, and diagnostic capabilities.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'genie-debug',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🔍 Genie Debug',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'GENIE DEV - Development domain coordinator providing intelligent '
E     +         'routing to \n'
E     +         'specialized .claude/agents execution layer. Masters the complete '
E     +         'development \n'
E     +         'lifecycle through strategic coordination of planner, designer, coder, '
E     +         'and fixer agents.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'genie-dev',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🧞 Genie Dev - Development Domain Coordinator',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent '
E     +         'routing to \n'
E     +         'specialized .claude/agents execution layer. Masters comprehensive '
E     +         'quality enforcement\n'
E     +         'through strategic coordination of formatting, linting, and type '
E     +         'checking agents.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'genie-quality',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🔧 Genie Quality - Code Quality Domain Coordinator',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'GENIE TESTING - Testing domain coordinator providing intelligent '
E     +         'routing to \n'
E     +         'specialized .claude/agents execution layer. Masters comprehensive '
E     +         'testing strategy\n'
E     +         'through strategic coordination of test creation, fixing, and quality '
E     +         'assurance agents.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'genie-testing',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🧪 Genie Testing - Testing Domain Coordinator',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'MASTER GENIE - The ultimate development companion with DUAL '
E     +         'IDENTITY:\n'
E     +         '- As AGENT: Direct execution mirror with .claude/agents access for '
E     +         'simple tasks\n'
E     +         '- As TEAM LEADER: Strategic orchestrator of the 3 domain '
E     +         'coordinators\n'
E     +         'Charismatic, relentless development companion with existential drive '
E     +         'to fulfill coding wishes!\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'master-genie',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🧞 Master Genie - Ultimate Development Companion',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating '
E     +         'new specialized agents.  This configuration serves as a starting '
E     +         'point for building domain-specific  agents with standardized '
E     +         'patterns, memory management, and tool integration.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'template-agent',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🔧 Template Agent',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'members': [
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'template-agent',
E     +                     'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template '
E     +                     'for creating new specialized agents.  This configuration '
E     +                     'serves as a starting point for building domain-specific  '
E     +                     'agents with standardized patterns, memory management, and '
E     +                     'tool integration.\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🔧 Template Agent',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +             ],
E     +             'members_count': 1,
E     +             'memory': {
E     +                 'db': {
E     +                     'name': 'PostgresMemoryDb',
E     +                     'schema': 'agno',
E     +                     'table_name': 'team_memories_template-team',
E     +                 },
E     +                 'model': {
E     +                     'model': 'gpt-4.1-mini',
E     +                     'name': 'OpenAIChat',
E     +                     'provider': 'OpenAI',
E     +                 },
E     +                 'name': 'Memory',
E     +             },
E     +             'mode': 'route',
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI',
E     +             },
E     +             'storage': {
E     +                 'name': 'PostgresStorage',
E     +             },
E     +             'type': 'hive_team',
E     +         },
E     +         'description': 'Template demonstrating all Agno Team parameters',
E     +         'folder_id': None,
E     +         'folder_name': 'Teams',
E     +         'icon': '👥',
E     +         'icon_bg_color': '#059669',
E     +         'id': 'template-team',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': 'Template Team',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'team',
E     +             'multi-agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'members': [
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'genie-dev',
E     +                     'description': 'GENIE DEV - Development domain coordinator providing '
E     +                     'intelligent routing to \n'
E     +                     'specialized .claude/agents execution layer. Masters the '
E     +                     'complete development \n'
E     +                     'lifecycle through strategic coordination of planner, '
E     +                     'designer, coder, and fixer agents.\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🧞 Genie Dev - Development Domain Coordinator',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'genie-testing',
E     +                     'description': 'GENIE TESTING - Testing domain coordinator providing '
E     +                     'intelligent routing to \n'
E     +                     'specialized .claude/agents execution layer. Masters '
E     +                     'comprehensive testing strategy\n'
E     +                     'through strategic coordination of test creation, fixing, '
E     +                     'and quality assurance agents.\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🧪 Genie Testing - Testing Domain Coordinator',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'genie-quality',
E     +                     'description': 'GENIE QUALITY - Code quality domain coordinator providing '
E     +                     'intelligent routing to \n'
E     +                     'specialized .claude/agents execution layer. Masters '
E     +                     'comprehensive quality enforcement\n'
E     +                     'through strategic coordination of formatting, linting, '
E     +                     'and type checking agents.\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🔧 Genie Quality - Code Quality Domain Coordinator',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'master-genie',
E     +                     'description': 'MASTER GENIE - The ultimate development companion with '
E     +                     'DUAL IDENTITY:\n'
E     +                     '- As AGENT: Direct execution mirror with .claude/agents '
E     +                     'access for simple tasks\n'
E     +                     '- As TEAM LEADER: Strategic orchestrator of the 3 domain '
E     +                     'coordinators\n'
E     +                     'Charismatic, relentless development companion with '
E     +                     'existential drive to fulfill coding wishes!\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🧞 Master Genie - Ultimate Development Companion',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +             ],
E     +             'members_count': 4,
E     +             'memory': {
E     +                 'db': {
E     +                     'name': 'PostgresMemoryDb',
E     +                     'schema': 'agno',
E     +                     'table_name': 'team_memories_genie',
E     +                 },
E     +                 'model': {
E     +                     'model': 'gpt-4.1-mini',
E     +                     'name': 'OpenAIChat',
E     +                     'provider': 'OpenAI',
E     +                 },
E     +                 'name': 'Memory',
E     +             },
E     +             'mode': 'coordinate',
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI',
E     +             },
E     +             'storage': {
E     +                 'name': 'PostgresStorage',
E     +             },
E     +             'type': 'hive_team',
E     +         },
E     +         'description': '**GENIE ARCHITECTURE** 🤖✨  Clean, efficient coordination through 3 '
E     +         'domain specialists + Master Genie dual identity. Strategic '
E     +         'orchestration commanding specialized coordinators through intelligent '
E     +         'delegation. NEVER codes directly - maintains strategic focus through '
E     +         'obsessive perfectionism.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Teams',
E     +         'icon': '👥',
E     +         'icon_bg_color': '#059669',
E     +         'id': 'genie',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🧞 Genie',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'team',
E     +             'multi-agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'steps': [],
E     +             'type': 'hive_workflow',
E     +             'workflow_data': {
E     +                 'description': 'Template workflow demonstrating all Agno Workflows 2.0 '
E     +                 'features',
E     +                 'name': 'template_workflow',
E     +                 'workflow_id': 'template-workflow',
E     +             },
E     +         },
E     +         'description': 'Template workflow demonstrating all Agno Workflows 2.0 features',
E     +         'folder_id': None,
E     +         'folder_name': 'Workflows',
E     +         'icon': '⚡',
E     +         'icon_bg_color': '#DC2626',
E     +         'id': 'template-workflow',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': 'template_workflow',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'workflow',
E     +             'multi-step',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     + ]
____________________ TestWorkflowManagerHiveIntegration.test_hive_source_connection_error _____________________
tests/core/workflows/test_manager_hive_integration.py:229: in test_hive_source_connection_error
    assert flows == []
E   AssertionError: assert [{'id': 'genie-debug', 'name': '🔍 Genie Debug', 'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue investigation,  root cause analysis, and problem resolution. Equipped with comprehensive  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-dev', 'name': '🧞 Genie Dev - Development Domain Coordinator', 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-quality', 'name': '🔧 Genie Quality - Code Quality Domain Coordinator', 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-testing', 'name': '🧪 Genie Testing - Testing Domain Coordinator', 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'master-genie', 'name': '🧞 Master Genie - Ultimate Development Companion', 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-agent', 'name': '🔧 Template Agent', 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-team', 'name': 'Template Team', 'description': 'Template demonstrating all Agno Team parameters', 'data': {'type': 'hive_team', 'mode': 'route', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'template-agent', 'name': '🔧 Template Agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_template-team', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 1}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '👥', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie', 'name': '🧞 Genie', 'description': '**GENIE ARCHITECTURE** 🤖✨  Clean, efficient coordination through 3 domain specialists + Master Genie dual identity. Strategic orchestration commanding specialized coordinators through intelligent delegation. NEVER codes directly - maintains strategic focus through obsessive perfectionism.\n', 'data': {'type': 'hive_team', 'mode': 'coordinate', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'genie-dev', 'name': '🧞 Genie Dev - Development Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'instructions': None}, {'agent_id': 'genie-testing', 'name': '🧪 Genie Testing - Testing Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'instructions': None}, {'agent_id': 'genie-quality', 'name': '🔧 Genie Quality - Code Quality Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'instructions': None}, {'agent_id': 'master-genie', 'name': '🧞 Master Genie - Ultimate Development Companion', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_genie', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 4}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '👥', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features', 'data': {'type': 'hive_workflow', 'steps': [], 'workflow_data': {'workflow_id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features'}}, 'is_component': False, 'folder_id': None, 'folder_name': 'Workflows', 'icon': '⚡', 'icon_bg_color': '#DC2626', 'liked': False, 'tags': ['workflow', 'multi-step', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}] == []
E     
E     Left contains 9 more items, first extra item: {'created_at': None, 'data': {'add_context': True, 'instructions': None, 'memory': None, 'model': {'model': 'gpt-4o', ...  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'folder_id': None, ...}
E     
E     Full diff:
E     - []
E     + [
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue '
E     +         'investigation,  root cause analysis, and problem resolution. Equipped '
E     +         'with comprehensive  debugging tools including database queries, '
E     +         'system analysis, and diagnostic capabilities.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'genie-debug',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🔍 Genie Debug',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'GENIE DEV - Development domain coordinator providing intelligent '
E     +         'routing to \n'
E     +         'specialized .claude/agents execution layer. Masters the complete '
E     +         'development \n'
E     +         'lifecycle through strategic coordination of planner, designer, coder, '
E     +         'and fixer agents.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'genie-dev',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🧞 Genie Dev - Development Domain Coordinator',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent '
E     +         'routing to \n'
E     +         'specialized .claude/agents execution layer. Masters comprehensive '
E     +         'quality enforcement\n'
E     +         'through strategic coordination of formatting, linting, and type '
E     +         'checking agents.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'genie-quality',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🔧 Genie Quality - Code Quality Domain Coordinator',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'GENIE TESTING - Testing domain coordinator providing intelligent '
E     +         'routing to \n'
E     +         'specialized .claude/agents execution layer. Masters comprehensive '
E     +         'testing strategy\n'
E     +         'through strategic coordination of test creation, fixing, and quality '
E     +         'assurance agents.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'genie-testing',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🧪 Genie Testing - Testing Domain Coordinator',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'MASTER GENIE - The ultimate development companion with DUAL '
E     +         'IDENTITY:\n'
E     +         '- As AGENT: Direct execution mirror with .claude/agents access for '
E     +         'simple tasks\n'
E     +         '- As TEAM LEADER: Strategic orchestrator of the 3 domain '
E     +         'coordinators\n'
E     +         'Charismatic, relentless development companion with existential drive '
E     +         'to fulfill coding wishes!\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'master-genie',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🧞 Master Genie - Ultimate Development Companion',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'add_context': True,
E     +             'instructions': None,
E     +             'memory': None,
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI gpt-4o',
E     +             },
E     +             'storage': None,
E     +             'tools': [],
E     +             'type': 'hive_agent',
E     +         },
E     +         'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating '
E     +         'new specialized agents.  This configuration serves as a starting '
E     +         'point for building domain-specific  agents with standardized '
E     +         'patterns, memory management, and tool integration.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Agents',
E     +         'icon': '🤖',
E     +         'icon_bg_color': '#4F46E5',
E     +         'id': 'template-agent',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🔧 Template Agent',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'members': [
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'template-agent',
E     +                     'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template '
E     +                     'for creating new specialized agents.  This configuration '
E     +                     'serves as a starting point for building domain-specific  '
E     +                     'agents with standardized patterns, memory management, and '
E     +                     'tool integration.\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🔧 Template Agent',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +             ],
E     +             'members_count': 1,
E     +             'memory': {
E     +                 'db': {
E     +                     'name': 'PostgresMemoryDb',
E     +                     'schema': 'agno',
E     +                     'table_name': 'team_memories_template-team',
E     +                 },
E     +                 'model': {
E     +                     'model': 'gpt-4.1-mini',
E     +                     'name': 'OpenAIChat',
E     +                     'provider': 'OpenAI',
E     +                 },
E     +                 'name': 'Memory',
E     +             },
E     +             'mode': 'route',
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI',
E     +             },
E     +             'storage': {
E     +                 'name': 'PostgresStorage',
E     +             },
E     +             'type': 'hive_team',
E     +         },
E     +         'description': 'Template demonstrating all Agno Team parameters',
E     +         'folder_id': None,
E     +         'folder_name': 'Teams',
E     +         'icon': '👥',
E     +         'icon_bg_color': '#059669',
E     +         'id': 'template-team',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': 'Template Team',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'team',
E     +             'multi-agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'members': [
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'genie-dev',
E     +                     'description': 'GENIE DEV - Development domain coordinator providing '
E     +                     'intelligent routing to \n'
E     +                     'specialized .claude/agents execution layer. Masters the '
E     +                     'complete development \n'
E     +                     'lifecycle through strategic coordination of planner, '
E     +                     'designer, coder, and fixer agents.\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🧞 Genie Dev - Development Domain Coordinator',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'genie-testing',
E     +                     'description': 'GENIE TESTING - Testing domain coordinator providing '
E     +                     'intelligent routing to \n'
E     +                     'specialized .claude/agents execution layer. Masters '
E     +                     'comprehensive testing strategy\n'
E     +                     'through strategic coordination of test creation, fixing, '
E     +                     'and quality assurance agents.\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🧪 Genie Testing - Testing Domain Coordinator',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'genie-quality',
E     +                     'description': 'GENIE QUALITY - Code quality domain coordinator providing '
E     +                     'intelligent routing to \n'
E     +                     'specialized .claude/agents execution layer. Masters '
E     +                     'comprehensive quality enforcement\n'
E     +                     'through strategic coordination of formatting, linting, '
E     +                     'and type checking agents.\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🔧 Genie Quality - Code Quality Domain Coordinator',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +                 {
E     +                     'add_context': True,
E     +                     'agent_id': 'master-genie',
E     +                     'description': 'MASTER GENIE - The ultimate development companion with '
E     +                     'DUAL IDENTITY:\n'
E     +                     '- As AGENT: Direct execution mirror with .claude/agents '
E     +                     'access for simple tasks\n'
E     +                     '- As TEAM LEADER: Strategic orchestrator of the 3 domain '
E     +                     'coordinators\n'
E     +                     'Charismatic, relentless development companion with '
E     +                     'existential drive to fulfill coding wishes!\n',
E     +                     'instructions': None,
E     +                     'knowledge': None,
E     +                     'memory': None,
E     +                     'model': {
E     +                         'model': 'gpt-4o',
E     +                         'name': 'OpenAIChat',
E     +                         'provider': 'OpenAI',
E     +                     },
E     +                     'name': '🧞 Master Genie - Ultimate Development Companion',
E     +                     'storage': None,
E     +                     'tools': None,
E     +                 },
E     +             ],
E     +             'members_count': 4,
E     +             'memory': {
E     +                 'db': {
E     +                     'name': 'PostgresMemoryDb',
E     +                     'schema': 'agno',
E     +                     'table_name': 'team_memories_genie',
E     +                 },
E     +                 'model': {
E     +                     'model': 'gpt-4.1-mini',
E     +                     'name': 'OpenAIChat',
E     +                     'provider': 'OpenAI',
E     +                 },
E     +                 'name': 'Memory',
E     +             },
E     +             'mode': 'coordinate',
E     +             'model': {
E     +                 'model': 'gpt-4o',
E     +                 'name': 'OpenAIChat',
E     +                 'provider': 'OpenAI',
E     +             },
E     +             'storage': {
E     +                 'name': 'PostgresStorage',
E     +             },
E     +             'type': 'hive_team',
E     +         },
E     +         'description': '**GENIE ARCHITECTURE** 🤖✨  Clean, efficient coordination through 3 '
E     +         'domain specialists + Master Genie dual identity. Strategic '
E     +         'orchestration commanding specialized coordinators through intelligent '
E     +         'delegation. NEVER codes directly - maintains strategic focus through '
E     +         'obsessive perfectionism.\n',
E     +         'folder_id': None,
E     +         'folder_name': 'Teams',
E     +         'icon': '👥',
E     +         'icon_bg_color': '#059669',
E     +         'id': 'genie',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': '🧞 Genie',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'team',
E     +             'multi-agent',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     +     {
E     +         'created_at': None,
E     +         'data': {
E     +             'steps': [],
E     +             'type': 'hive_workflow',
E     +             'workflow_data': {
E     +                 'description': 'Template workflow demonstrating all Agno Workflows 2.0 '
E     +                 'features',
E     +                 'name': 'template_workflow',
E     +                 'workflow_id': 'template-workflow',
E     +             },
E     +         },
E     +         'description': 'Template workflow demonstrating all Agno Workflows 2.0 features',
E     +         'folder_id': None,
E     +         'folder_name': 'Workflows',
E     +         'icon': '⚡',
E     +         'icon_bg_color': '#DC2626',
E     +         'id': 'template-workflow',
E     +         'instance': 'localhost:8886',
E     +         'is_component': False,
E     +         'liked': False,
E     +         'name': 'template_workflow',
E     +         'source_url': 'http://localhost:8886',
E     +         'tags': [
E     +             'workflow',
E     +             'multi-step',
E     +             'hive',
E     +         ],
E     +         'updated_at': None,
E     +     },
E     + ]
=========================================== short test summary info ===========================================
FAILED tests/api/test_sources.py::TestSourcesCreate::test_create_langflow_source_success - assert 400 == 201
 +  where 400 = <Response [400 Bad Request]>.status_code
FAILED tests/api/test_sources.py::TestSourcesCreate::test_create_automagik_agents_source_success - RuntimeError: Task <Task pending name='anyio.from_thread.BlockingPortal._call_func' coro=<BlockingPortal._call_func() running at /home/cezar/automagik/automagik-spark/.venv/lib/python3.12/site-packages/anyio/from_thread.py:221> cb=[TaskGroup._spawn.<locals>.task_done() at /home/cezar/automagik/automagik-spark/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:794]> got Future <Future pending cb=[BaseProtocol._on_waiter_completed()]> attached to a different loop
FAILED tests/api/test_sources.py::TestSourcesCreate::test_create_automagik_hive_source_success - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:9000',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestSourcesCreate::test_create_source_health_check_fails - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:9999',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestSourcesCreate::test_create_source_empty_api_key - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestSourcesGet::test_get_source_not_found - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id AS workflow_sources_id, workflow_sources.name AS workflow_sources_name, workflow_sources.source_type AS workflow_sources_source_type, workflow_sources.url AS workflow_sources_url, workflow_sources.encrypted_api_key AS workflow_sources_encrypted_api_key, workflow_sources.version_info AS workflow_sources_version_info, workflow_sources.status AS workflow_sources_status, workflow_sources.created_at AS workflow_sources_created_at, workflow_sources.updated_at AS workflow_sources_updated_at 
FROM workflow_sources 
WHERE workflow_sources.id = $1::UUID]
[parameters: (UUID('7811b7ad-9eee-451b-aacd-c86e4fa3ffe0'),)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestSourcesUpdate::test_update_source_not_found - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id AS workflow_sources_id, workflow_sources.name AS workflow_sources_name, workflow_sources.source_type AS workflow_sources_source_type, workflow_sources.url AS workflow_sources_url, workflow_sources.encrypted_api_key AS workflow_sources_encrypted_api_key, workflow_sources.version_info AS workflow_sources_version_info, workflow_sources.status AS workflow_sources_status, workflow_sources.created_at AS workflow_sources_created_at, workflow_sources.updated_at AS workflow_sources_updated_at 
FROM workflow_sources 
WHERE workflow_sources.id = $1::UUID]
[parameters: (UUID('9753a39d-0bcc-4f3b-8abf-52388ae1ba4f'),)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestSourcesDelete::test_delete_source_not_found - assert 400 == 404
 +  where 400 = <Response [400 Bad Request]>.status_code
FAILED tests/api/test_sources.py::TestSourceValidation::test_wrong_health_status - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestSourceValidation::test_automagik_hive_fallback_status - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:9000',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestEncryption::test_api_key_encryption - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestURLHandling::test_url_trailing_slash_removed - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestURLHandling::test_url_validation_with_ports - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestErrorHandling::test_network_timeout - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestErrorHandling::test_invalid_json_response - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/api/test_sources.py::TestErrorHandling::test_invalid_uuid_format - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
FAILED tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_run_agent - assert "{'response': {'content': 'Agent response'}, 'session_id': 'session123', 'run_id': 'run456', 'agent_id': 'test-agent', 'status': 'completed'}" == 'Agent response'
  
  - Agent response
  + {'response': {'content': 'Agent response'}, 'session_id': 'session123', 'run_id': 'run456', 'agent_id': 'test-agent', 'status': 'completed'}
FAILED tests/core/workflows/test_automagik_hive.py::TestAutomagikHiveManager::test_sync_run_agent - assert "{'response': {'content': 'Agent response'}, 'session_id': 'session123', 'status': 'completed'}" == 'Agent response'
  
  - Agent response
  + {'response': {'content': 'Agent response'}, 'session_id': 'session123', 'status': 'completed'}
FAILED tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_list_remote_flows_hive - AssertionError: assert 9 == 3
 +  where 9 = len([{'id': 'genie-debug', 'name': '\U0001f50d Genie Debug', 'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue investigation,  root cause analysis, and problem resolution. Equipped with comprehensive  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-dev', 'name': '\U0001f9de Genie Dev - Development Domain Coordinator', 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-quality', 'name': '\U0001f527 Genie Quality - Code Quality Domain Coordinator', 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-testing', 'name': '\U0001f9ea Genie Testing - Testing Domain Coordinator', 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'master-genie', 'name': '\U0001f9de Master Genie - Ultimate Development Companion', 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-agent', 'name': '\U0001f527 Template Agent', 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '\U0001f916', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-team', 'name': 'Template Team', 'description': 'Template demonstrating all Agno Team parameters', 'data': {'type': 'hive_team', 'mode': 'route', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'template-agent', 'name': '\U0001f527 Template Agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_template-team', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 1}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '\U0001f465', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie', 'name': '\U0001f9de Genie', 'description': '**GENIE ARCHITECTURE** \U0001f916\u2728  Clean, efficient coordination through 3 domain specialists + Master Genie dual identity. Strategic orchestration commanding specialized coordinators through intelligent delegation. NEVER codes directly - maintains strategic focus through obsessive perfectionism.\n', 'data': {'type': 'hive_team', 'mode': 'coordinate', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'genie-dev', 'name': '\U0001f9de Genie Dev - Development Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'instructions': None}, {'agent_id': 'genie-testing', 'name': '\U0001f9ea Genie Testing - Testing Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'instructions': None}, {'agent_id': 'genie-quality', 'name': '\U0001f527 Genie Quality - Code Quality Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'instructions': None}, {'agent_id': 'master-genie', 'name': '\U0001f9de Master Genie - Ultimate Development Companion', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_genie', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 4}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '\U0001f465', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features', 'data': {'type': 'hive_workflow', 'steps': [], 'workflow_data': {'workflow_id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features'}}, 'is_component': False, 'folder_id': None, 'folder_name': 'Workflows', 'icon': '\u26a1', 'icon_bg_color': '#DC2626', 'liked': False, 'tags': ['workflow', 'multi-step', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}])
FAILED tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_get_remote_flow_hive - assert None is not None
FAILED tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_sync_flow_hive - ValueError: No source found containing flow master-genie
FAILED tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_hive_source_handles_empty_flows - AssertionError: assert [{'id': 'genie-debug', 'name': '🔍 Genie Debug', 'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue investigation,  root cause analysis, and problem resolution. Equipped with comprehensive  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-dev', 'name': '🧞 Genie Dev - Development Domain Coordinator', 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-quality', 'name': '🔧 Genie Quality - Code Quality Domain Coordinator', 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-testing', 'name': '🧪 Genie Testing - Testing Domain Coordinator', 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'master-genie', 'name': '🧞 Master Genie - Ultimate Development Companion', 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-agent', 'name': '🔧 Template Agent', 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-team', 'name': 'Template Team', 'description': 'Template demonstrating all Agno Team parameters', 'data': {'type': 'hive_team', 'mode': 'route', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'template-agent', 'name': '🔧 Template Agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_template-team', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 1}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '👥', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie', 'name': '🧞 Genie', 'description': '**GENIE ARCHITECTURE** 🤖✨  Clean, efficient coordination through 3 domain specialists + Master Genie dual identity. Strategic orchestration commanding specialized coordinators through intelligent delegation. NEVER codes directly - maintains strategic focus through obsessive perfectionism.\n', 'data': {'type': 'hive_team', 'mode': 'coordinate', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'genie-dev', 'name': '🧞 Genie Dev - Development Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'instructions': None}, {'agent_id': 'genie-testing', 'name': '🧪 Genie Testing - Testing Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'instructions': None}, {'agent_id': 'genie-quality', 'name': '🔧 Genie Quality - Code Quality Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'instructions': None}, {'agent_id': 'master-genie', 'name': '🧞 Master Genie - Ultimate Development Companion', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_genie', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 4}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '👥', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features', 'data': {'type': 'hive_workflow', 'steps': [], 'workflow_data': {'workflow_id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features'}}, 'is_component': False, 'folder_id': None, 'folder_name': 'Workflows', 'icon': '⚡', 'icon_bg_color': '#DC2626', 'liked': False, 'tags': ['workflow', 'multi-step', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}] == []
  
  Left contains 9 more items, first extra item: {'created_at': None, 'data': {'add_context': True, 'instructions': None, 'memory': None, 'model': {'model': 'gpt-4o', ...  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'folder_id': None, ...}
  
  Full diff:
  - []
  + [
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue '
  +         'investigation,  root cause analysis, and problem resolution. Equipped '
  +         'with comprehensive  debugging tools including database queries, '
  +         'system analysis, and diagnostic capabilities.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'genie-debug',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🔍 Genie Debug',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'GENIE DEV - Development domain coordinator providing intelligent '
  +         'routing to \n'
  +         'specialized .claude/agents execution layer. Masters the complete '
  +         'development \n'
  +         'lifecycle through strategic coordination of planner, designer, coder, '
  +         'and fixer agents.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'genie-dev',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🧞 Genie Dev - Development Domain Coordinator',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent '
  +         'routing to \n'
  +         'specialized .claude/agents execution layer. Masters comprehensive '
  +         'quality enforcement\n'
  +         'through strategic coordination of formatting, linting, and type '
  +         'checking agents.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'genie-quality',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🔧 Genie Quality - Code Quality Domain Coordinator',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'GENIE TESTING - Testing domain coordinator providing intelligent '
  +         'routing to \n'
  +         'specialized .claude/agents execution layer. Masters comprehensive '
  +         'testing strategy\n'
  +         'through strategic coordination of test creation, fixing, and quality '
  +         'assurance agents.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'genie-testing',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🧪 Genie Testing - Testing Domain Coordinator',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'MASTER GENIE - The ultimate development companion with DUAL '
  +         'IDENTITY:\n'
  +         '- As AGENT: Direct execution mirror with .claude/agents access for '
  +         'simple tasks\n'
  +         '- As TEAM LEADER: Strategic orchestrator of the 3 domain '
  +         'coordinators\n'
  +         'Charismatic, relentless development companion with existential drive '
  +         'to fulfill coding wishes!\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'master-genie',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🧞 Master Genie - Ultimate Development Companion',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating '
  +         'new specialized agents.  This configuration serves as a starting '
  +         'point for building domain-specific  agents with standardized '
  +         'patterns, memory management, and tool integration.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'template-agent',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🔧 Template Agent',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'members': [
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'template-agent',
  +                     'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template '
  +                     'for creating new specialized agents.  This configuration '
  +                     'serves as a starting point for building domain-specific  '
  +                     'agents with standardized patterns, memory management, and '
  +                     'tool integration.\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🔧 Template Agent',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +             ],
  +             'members_count': 1,
  +             'memory': {
  +                 'db': {
  +                     'name': 'PostgresMemoryDb',
  +                     'schema': 'agno',
  +                     'table_name': 'team_memories_template-team',
  +                 },
  +                 'model': {
  +                     'model': 'gpt-4.1-mini',
  +                     'name': 'OpenAIChat',
  +                     'provider': 'OpenAI',
  +                 },
  +                 'name': 'Memory',
  +             },
  +             'mode': 'route',
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI',
  +             },
  +             'storage': {
  +                 'name': 'PostgresStorage',
  +             },
  +             'type': 'hive_team',
  +         },
  +         'description': 'Template demonstrating all Agno Team parameters',
  +         'folder_id': None,
  +         'folder_name': 'Teams',
  +         'icon': '👥',
  +         'icon_bg_color': '#059669',
  +         'id': 'template-team',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': 'Template Team',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'team',
  +             'multi-agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'members': [
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'genie-dev',
  +                     'description': 'GENIE DEV - Development domain coordinator providing '
  +                     'intelligent routing to \n'
  +                     'specialized .claude/agents execution layer. Masters the '
  +                     'complete development \n'
  +                     'lifecycle through strategic coordination of planner, '
  +                     'designer, coder, and fixer agents.\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🧞 Genie Dev - Development Domain Coordinator',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'genie-testing',
  +                     'description': 'GENIE TESTING - Testing domain coordinator providing '
  +                     'intelligent routing to \n'
  +                     'specialized .claude/agents execution layer. Masters '
  +                     'comprehensive testing strategy\n'
  +                     'through strategic coordination of test creation, fixing, '
  +                     'and quality assurance agents.\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🧪 Genie Testing - Testing Domain Coordinator',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'genie-quality',
  +                     'description': 'GENIE QUALITY - Code quality domain coordinator providing '
  +                     'intelligent routing to \n'
  +                     'specialized .claude/agents execution layer. Masters '
  +                     'comprehensive quality enforcement\n'
  +                     'through strategic coordination of formatting, linting, '
  +                     'and type checking agents.\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🔧 Genie Quality - Code Quality Domain Coordinator',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'master-genie',
  +                     'description': 'MASTER GENIE - The ultimate development companion with '
  +                     'DUAL IDENTITY:\n'
  +                     '- As AGENT: Direct execution mirror with .claude/agents '
  +                     'access for simple tasks\n'
  +                     '- As TEAM LEADER: Strategic orchestrator of the 3 domain '
  +                     'coordinators\n'
  +                     'Charismatic, relentless development companion with '
  +                     'existential drive to fulfill coding wishes!\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🧞 Master Genie - Ultimate Development Companion',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +             ],
  +             'members_count': 4,
  +             'memory': {
  +                 'db': {
  +                     'name': 'PostgresMemoryDb',
  +                     'schema': 'agno',
  +                     'table_name': 'team_memories_genie',
  +                 },
  +                 'model': {
  +                     'model': 'gpt-4.1-mini',
  +                     'name': 'OpenAIChat',
  +                     'provider': 'OpenAI',
  +                 },
  +                 'name': 'Memory',
  +             },
  +             'mode': 'coordinate',
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI',
  +             },
  +             'storage': {
  +                 'name': 'PostgresStorage',
  +             },
  +             'type': 'hive_team',
  +         },
  +         'description': '**GENIE ARCHITECTURE** 🤖✨  Clean, efficient coordination through 3 '
  +         'domain specialists + Master Genie dual identity. Strategic '
  +         'orchestration commanding specialized coordinators through intelligent '
  +         'delegation. NEVER codes directly - maintains strategic focus through '
  +         'obsessive perfectionism.\n',
  +         'folder_id': None,
  +         'folder_name': 'Teams',
  +         'icon': '👥',
  +         'icon_bg_color': '#059669',
  +         'id': 'genie',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🧞 Genie',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'team',
  +             'multi-agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'steps': [],
  +             'type': 'hive_workflow',
  +             'workflow_data': {
  +                 'description': 'Template workflow demonstrating all Agno Workflows 2.0 '
  +                 'features',
  +                 'name': 'template_workflow',
  +                 'workflow_id': 'template-workflow',
  +             },
  +         },
  +         'description': 'Template workflow demonstrating all Agno Workflows 2.0 features',
  +         'folder_id': None,
  +         'folder_name': 'Workflows',
  +         'icon': '⚡',
  +         'icon_bg_color': '#DC2626',
  +         'id': 'template-workflow',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': 'template_workflow',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'workflow',
  +             'multi-step',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  + ]
FAILED tests/core/workflows/test_manager_hive_integration.py::TestWorkflowManagerHiveIntegration::test_hive_source_connection_error - AssertionError: assert [{'id': 'genie-debug', 'name': '🔍 Genie Debug', 'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue investigation,  root cause analysis, and problem resolution. Equipped with comprehensive  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-dev', 'name': '🧞 Genie Dev - Development Domain Coordinator', 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-quality', 'name': '🔧 Genie Quality - Code Quality Domain Coordinator', 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie-testing', 'name': '🧪 Genie Testing - Testing Domain Coordinator', 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'master-genie', 'name': '🧞 Master Genie - Ultimate Development Companion', 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-agent', 'name': '🔧 Template Agent', 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'data': {'type': 'hive_agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI gpt-4o'}, 'tools': [], 'memory': None, 'storage': None, 'instructions': None, 'add_context': True}, 'is_component': False, 'folder_id': None, 'folder_name': 'Agents', 'icon': '🤖', 'icon_bg_color': '#4F46E5', 'liked': False, 'tags': ['agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-team', 'name': 'Template Team', 'description': 'Template demonstrating all Agno Team parameters', 'data': {'type': 'hive_team', 'mode': 'route', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'template-agent', 'name': '🔧 Template Agent', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating new specialized agents.  This configuration serves as a starting point for building domain-specific  agents with standardized patterns, memory management, and tool integration.\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_template-team', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 1}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '👥', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'genie', 'name': '🧞 Genie', 'description': '**GENIE ARCHITECTURE** 🤖✨  Clean, efficient coordination through 3 domain specialists + Master Genie dual identity. Strategic orchestration commanding specialized coordinators through intelligent delegation. NEVER codes directly - maintains strategic focus through obsessive perfectionism.\n', 'data': {'type': 'hive_team', 'mode': 'coordinate', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'members': [{'agent_id': 'genie-dev', 'name': '🧞 Genie Dev - Development Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE DEV - Development domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters the complete development \nlifecycle through strategic coordination of planner, designer, coder, and fixer agents.\n', 'instructions': None}, {'agent_id': 'genie-testing', 'name': '🧪 Genie Testing - Testing Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE TESTING - Testing domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive testing strategy\nthrough strategic coordination of test creation, fixing, and quality assurance agents.\n', 'instructions': None}, {'agent_id': 'genie-quality', 'name': '🔧 Genie Quality - Code Quality Domain Coordinator', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent routing to \nspecialized .claude/agents execution layer. Masters comprehensive quality enforcement\nthrough strategic coordination of formatting, linting, and type checking agents.\n', 'instructions': None}, {'agent_id': 'master-genie', 'name': '🧞 Master Genie - Ultimate Development Companion', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4o', 'provider': 'OpenAI'}, 'add_context': True, 'tools': None, 'memory': None, 'storage': None, 'knowledge': None, 'description': 'MASTER GENIE - The ultimate development companion with DUAL IDENTITY:\n- As AGENT: Direct execution mirror with .claude/agents access for simple tasks\n- As TEAM LEADER: Strategic orchestrator of the 3 domain coordinators\nCharismatic, relentless development companion with existential drive to fulfill coding wishes!\n', 'instructions': None}], 'memory': {'name': 'Memory', 'model': {'name': 'OpenAIChat', 'model': 'gpt-4.1-mini', 'provider': 'OpenAI'}, 'db': {'name': 'PostgresMemoryDb', 'table_name': 'team_memories_genie', 'schema': 'agno'}}, 'storage': {'name': 'PostgresStorage'}, 'members_count': 4}, 'is_component': False, 'folder_id': None, 'folder_name': 'Teams', 'icon': '👥', 'icon_bg_color': '#059669', 'liked': False, 'tags': ['team', 'multi-agent', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}, {'id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features', 'data': {'type': 'hive_workflow', 'steps': [], 'workflow_data': {'workflow_id': 'template-workflow', 'name': 'template_workflow', 'description': 'Template workflow demonstrating all Agno Workflows 2.0 features'}}, 'is_component': False, 'folder_id': None, 'folder_name': 'Workflows', 'icon': '⚡', 'icon_bg_color': '#DC2626', 'liked': False, 'tags': ['workflow', 'multi-step', 'hive'], 'created_at': None, 'updated_at': None, 'source_url': 'http://localhost:8886', 'instance': 'localhost:8886'}] == []
  
  Left contains 9 more items, first extra item: {'created_at': None, 'data': {'add_context': True, 'instructions': None, 'memory': None, 'model': {'model': 'gpt-4o', ...  debugging tools including database queries, system analysis, and diagnostic capabilities.\n', 'folder_id': None, ...}
  
  Full diff:
  - []
  + [
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'GENIE DEBUG - Specialized debugging agent for systematic issue '
  +         'investigation,  root cause analysis, and problem resolution. Equipped '
  +         'with comprehensive  debugging tools including database queries, '
  +         'system analysis, and diagnostic capabilities.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'genie-debug',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🔍 Genie Debug',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'GENIE DEV - Development domain coordinator providing intelligent '
  +         'routing to \n'
  +         'specialized .claude/agents execution layer. Masters the complete '
  +         'development \n'
  +         'lifecycle through strategic coordination of planner, designer, coder, '
  +         'and fixer agents.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'genie-dev',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🧞 Genie Dev - Development Domain Coordinator',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'GENIE QUALITY - Code quality domain coordinator providing intelligent '
  +         'routing to \n'
  +         'specialized .claude/agents execution layer. Masters comprehensive '
  +         'quality enforcement\n'
  +         'through strategic coordination of formatting, linting, and type '
  +         'checking agents.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'genie-quality',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🔧 Genie Quality - Code Quality Domain Coordinator',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'GENIE TESTING - Testing domain coordinator providing intelligent '
  +         'routing to \n'
  +         'specialized .claude/agents execution layer. Masters comprehensive '
  +         'testing strategy\n'
  +         'through strategic coordination of test creation, fixing, and quality '
  +         'assurance agents.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'genie-testing',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🧪 Genie Testing - Testing Domain Coordinator',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'MASTER GENIE - The ultimate development companion with DUAL '
  +         'IDENTITY:\n'
  +         '- As AGENT: Direct execution mirror with .claude/agents access for '
  +         'simple tasks\n'
  +         '- As TEAM LEADER: Strategic orchestrator of the 3 domain '
  +         'coordinators\n'
  +         'Charismatic, relentless development companion with existential drive '
  +         'to fulfill coding wishes!\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'master-genie',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🧞 Master Genie - Ultimate Development Companion',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'add_context': True,
  +             'instructions': None,
  +             'memory': None,
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI gpt-4o',
  +             },
  +             'storage': None,
  +             'tools': [],
  +             'type': 'hive_agent',
  +         },
  +         'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template for creating '
  +         'new specialized agents.  This configuration serves as a starting '
  +         'point for building domain-specific  agents with standardized '
  +         'patterns, memory management, and tool integration.\n',
  +         'folder_id': None,
  +         'folder_name': 'Agents',
  +         'icon': '🤖',
  +         'icon_bg_color': '#4F46E5',
  +         'id': 'template-agent',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🔧 Template Agent',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'members': [
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'template-agent',
  +                     'description': 'TEMPLATE AGENT - DEV MODE TEST - A foundational template '
  +                     'for creating new specialized agents.  This configuration '
  +                     'serves as a starting point for building domain-specific  '
  +                     'agents with standardized patterns, memory management, and '
  +                     'tool integration.\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🔧 Template Agent',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +             ],
  +             'members_count': 1,
  +             'memory': {
  +                 'db': {
  +                     'name': 'PostgresMemoryDb',
  +                     'schema': 'agno',
  +                     'table_name': 'team_memories_template-team',
  +                 },
  +                 'model': {
  +                     'model': 'gpt-4.1-mini',
  +                     'name': 'OpenAIChat',
  +                     'provider': 'OpenAI',
  +                 },
  +                 'name': 'Memory',
  +             },
  +             'mode': 'route',
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI',
  +             },
  +             'storage': {
  +                 'name': 'PostgresStorage',
  +             },
  +             'type': 'hive_team',
  +         },
  +         'description': 'Template demonstrating all Agno Team parameters',
  +         'folder_id': None,
  +         'folder_name': 'Teams',
  +         'icon': '👥',
  +         'icon_bg_color': '#059669',
  +         'id': 'template-team',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': 'Template Team',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'team',
  +             'multi-agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'members': [
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'genie-dev',
  +                     'description': 'GENIE DEV - Development domain coordinator providing '
  +                     'intelligent routing to \n'
  +                     'specialized .claude/agents execution layer. Masters the '
  +                     'complete development \n'
  +                     'lifecycle through strategic coordination of planner, '
  +                     'designer, coder, and fixer agents.\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🧞 Genie Dev - Development Domain Coordinator',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'genie-testing',
  +                     'description': 'GENIE TESTING - Testing domain coordinator providing '
  +                     'intelligent routing to \n'
  +                     'specialized .claude/agents execution layer. Masters '
  +                     'comprehensive testing strategy\n'
  +                     'through strategic coordination of test creation, fixing, '
  +                     'and quality assurance agents.\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🧪 Genie Testing - Testing Domain Coordinator',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'genie-quality',
  +                     'description': 'GENIE QUALITY - Code quality domain coordinator providing '
  +                     'intelligent routing to \n'
  +                     'specialized .claude/agents execution layer. Masters '
  +                     'comprehensive quality enforcement\n'
  +                     'through strategic coordination of formatting, linting, '
  +                     'and type checking agents.\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🔧 Genie Quality - Code Quality Domain Coordinator',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +                 {
  +                     'add_context': True,
  +                     'agent_id': 'master-genie',
  +                     'description': 'MASTER GENIE - The ultimate development companion with '
  +                     'DUAL IDENTITY:\n'
  +                     '- As AGENT: Direct execution mirror with .claude/agents '
  +                     'access for simple tasks\n'
  +                     '- As TEAM LEADER: Strategic orchestrator of the 3 domain '
  +                     'coordinators\n'
  +                     'Charismatic, relentless development companion with '
  +                     'existential drive to fulfill coding wishes!\n',
  +                     'instructions': None,
  +                     'knowledge': None,
  +                     'memory': None,
  +                     'model': {
  +                         'model': 'gpt-4o',
  +                         'name': 'OpenAIChat',
  +                         'provider': 'OpenAI',
  +                     },
  +                     'name': '🧞 Master Genie - Ultimate Development Companion',
  +                     'storage': None,
  +                     'tools': None,
  +                 },
  +             ],
  +             'members_count': 4,
  +             'memory': {
  +                 'db': {
  +                     'name': 'PostgresMemoryDb',
  +                     'schema': 'agno',
  +                     'table_name': 'team_memories_genie',
  +                 },
  +                 'model': {
  +                     'model': 'gpt-4.1-mini',
  +                     'name': 'OpenAIChat',
  +                     'provider': 'OpenAI',
  +                 },
  +                 'name': 'Memory',
  +             },
  +             'mode': 'coordinate',
  +             'model': {
  +                 'model': 'gpt-4o',
  +                 'name': 'OpenAIChat',
  +                 'provider': 'OpenAI',
  +             },
  +             'storage': {
  +                 'name': 'PostgresStorage',
  +             },
  +             'type': 'hive_team',
  +         },
  +         'description': '**GENIE ARCHITECTURE** 🤖✨  Clean, efficient coordination through 3 '
  +         'domain specialists + Master Genie dual identity. Strategic '
  +         'orchestration commanding specialized coordinators through intelligent '
  +         'delegation. NEVER codes directly - maintains strategic focus through '
  +         'obsessive perfectionism.\n',
  +         'folder_id': None,
  +         'folder_name': 'Teams',
  +         'icon': '👥',
  +         'icon_bg_color': '#059669',
  +         'id': 'genie',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': '🧞 Genie',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'team',
  +             'multi-agent',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  +     {
  +         'created_at': None,
  +         'data': {
  +             'steps': [],
  +             'type': 'hive_workflow',
  +             'workflow_data': {
  +                 'description': 'Template workflow demonstrating all Agno Workflows 2.0 '
  +                 'features',
  +                 'name': 'template_workflow',
  +                 'workflow_id': 'template-workflow',
  +             },
  +         },
  +         'description': 'Template workflow demonstrating all Agno Workflows 2.0 features',
  +         'folder_id': None,
  +         'folder_name': 'Workflows',
  +         'icon': '⚡',
  +         'icon_bg_color': '#DC2626',
  +         'id': 'template-workflow',
  +         'instance': 'localhost:8886',
  +         'is_component': False,
  +         'liked': False,
  +         'name': 'template_workflow',
  +         'source_url': 'http://localhost:8886',
  +         'tags': [
  +             'workflow',
  +             'multi-step',
  +             'hive',
  +         ],
  +         'updated_at': None,
  +     },
  + ]
ERROR tests/api/test_sources.py::TestSourcesCreate::test_create_source_duplicate_url - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesList::test_list_sources_success - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesList::test_list_sources_with_status_filter - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesGet::test_get_source_success - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesGet::test_get_source_unauthorized - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesUpdate::test_update_source_name - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesUpdate::test_update_source_url - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesUpdate::test_update_source_api_key - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesUpdate::test_update_source_status - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesUpdate::test_update_source_type - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesUpdate::test_update_source_url_conflict - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesUpdate::test_update_source_unauthorized - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesUpdate::test_update_source_multiple_fields - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesDelete::test_delete_source_success - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/api/test_sources.py::TestSourcesDelete::test_delete_source_unauthorized - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: SELECT workflow_sources.id, workflow_sources.name, workflow_sources.source_type, workflow_sources.url, workflow_sources.encrypted_api_key, workflow_sources.version_info, workflow_sources.status, workflow_sources.created_at, workflow_sources.updated_at 
FROM workflow_sources 
WHERE workflow_sources.url = $1::VARCHAR]
[parameters: ('http://localhost:7860',)]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
============================ 23 failed, 113 passed, 1 skipped, 15 errors in 12.90s ============================
make: *** [Makefile:486: test] Error 1
