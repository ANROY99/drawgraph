(SELECT
        dfla.source_order_number AS SRC_ORDER_NUM,
        (dla.display_line_number
        ||
        '-'
        ||
        dfla.fulfill_line_number) AS DISPLAY_LINE,
        dfla.fulfill_line_id    AS FULFILL_ID                ,
        dla.line_id             AS LINE_ID,
        dha.header_id           AS HDR_ID                  ,
        b.DOO_PROCESS_ID       AS DOO_PRC_ID                 ,
        dpdv.PROCESS_NAME      AS DOO_PRC_NAME                 ,
        b.step_number                    AS STEP_NUMBER       ,
        ins.ACTUAL_start_DATE    AS ACT_START_DATE               ,
        ins.ACTUAL_COMPLETION_DATE      AS ACT_COMPLETION_DATE        ,
        dttv.TASK_TYPE          AS TASK_TYPE                ,
        tl.step_name                 AS STEP_NAME           ,
        ins.step_status              AS STEP_STS           ,
        task.status_code      AS TASK_CODE       ,
        dha.order_number              AS ORDER_NUM          ,
        grps.group_id                        AS GRP_ID   ,
        ins.doo_process_instance_id     AS DOO_PRC_INST_ID        ,
        grps.creation_date                     AS CREATION_DATE ,
        grps.status                             AS STATUS,
        ins.doo_process_instance_id        AS DOO_PID ,
        ins.step_instance_id                 AS STEP_INST_ID   ,
        ins.task_instance_id                  AS TASK_INST_ID  ,
        tl.step_id                           AS STEP_ID   ,
        B.DEFAULT_EXIT_STATUS_CODE    AS DFLT_EXIT_STS_CODE          ,
        B.EXIT_CRITERIA_STATUS_CODE AS EXIT_CRITERIA_STS_CODE
FROM    doo_headers_all dha            ,
        doo_fulfill_lines_all dfla     ,
        doo_lines_all dla              ,
        doo_orchestration_groups grps  ,
        doo_process_step_instances ins ,
        doo_task_instances task        ,
        doo_process_steps_b b          ,
        doo_process_steps_tl tl        ,
        DOO_PROCESS_DEFINITIONS_VL dpdv,
        DOO_TASK_DEFINITIONS_VL dtdv   ,
        DOO_TASK_TYPES_VL dttv
WHERE   --dha.order_number IN ('1970')  AND 
        dha.submitted_flag   = 'Y'
        AND dha.header_id        = dfla.header_id
        AND dfla.line_id         = dla.line_id
        AND dha.header_id        = grps.header_id
        AND dfla.fulfill_line_id = grps.fulfillment_line_id
        AND grps.status          ='ACTIVE'
        AND grps.group_id        = ins.group_id
        AND ins.task_instance_id = task.task_instance_id
        AND ins.step_id          = b.step_id
        AND b.step_id            = tl.step_id
        AND TL.LANGUAGE          = 'US'
        AND dtdv.task_id         = task.task_id
        AND dtdv.task_type_id    = dttv.task_type_id
        AND b.DOO_PROCESS_ID     = dpdv.DOO_PROCESS_ID
        AND task.STEP_ACTIVE = 'ACTIVE'
)