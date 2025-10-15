(SELECT  dha.source_order_number AS SRC_ORD_NUM,
dha.order_number AS ORDER_NUM,
dha.header_id AS HDR_ID,
        (
                SELECT DISTINCT service_name
                FROM    fusion.DOO_SERVICE_DEFINITIONS_tl
                WHERE   service_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'SVC'
                                        AND language    = userenv('LANG')
                        )
       ) AS Service,
        (
                SELECT DISTINCT display_name
                FROM    fusion.DOO_TASK_INSTANCES sdti,
                        fusion.DOO_TASK_DEFINITIONS_TL sdtt
                WHERE   task_instance_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'TASK'
                                        AND language    = userenv('LANG')
                        )
                        AND sdti.task_id  = sdtt.task_id
                        AND sdtt.language = userenv('LANG')
        ) AS Task             ,
        dmr.REQUEST_FUNCTION AS REQ_FUNC,
        dmr.REQ_ENTITY_TYPE  AS NTT_TYPE,
        dmr.REQUEST_RESULT   AS REQ_RESULT,
        dmb.msg_entity_type  AS MSG_NTT_TYPE,
        dmb.msg_entity_id1   AS MSG_NTT_ID1,
        dmt.message_text     AS MSG_TEXT,
		dmt.creation_Date AS CREATION_DATE
FROM    fusion.DOO_MESSAGE_requests dmr   ,
        FUSION.DOO_MESSAGE_ENTITIES DME   ,
        fusion.DOO_MESSAGES_B DMB         ,
        fusion.DOO_MESSAGES_TL DMT        ,
        fusion.doo_headers_all dha        ,
        fusion.doo_lines_all dla          ,
        fusion.doo_fulfill_lines_all dfla ,
        FUSION.doo_ORCHESTRATION_GROUPS DOG
WHERE   dmr.MSG_REQUEST_ID                = DMB.MSG_REQUEST_ID
        AND dmr.ACTIVE_FLAG               = 'Y'
        AND DMB.msg_request_id            = DME.msg_request_id
        AND DMB.message_id                = DME.message_id
        AND DMT.message_id                = DMB.message_id
        AND dmt.language                  = userenv('LANG')
        AND dmb.MSG_ENTITY_TYPE          IN ('FLINE')
        AND dmb.msg_entity_type           = dme.ENTITY_NAME
        AND TO_CHAR(dfla.fulfill_line_id) = dmb.msg_entity_id1
        AND dha.header_id        = dfla.header_id
        AND dfla.line_id         = dla.line_id
        AND dfla.fulfill_line_id = dog.fulfillment_line_id
        AND dog.status           = 'ACTIVE'
        AND EXISTS
        (
                SELECT  1
                FROM    fusion.doo_process_step_instances dpsi
                WHERE
                       dog.group_id                 = dpsi.group_id
                        AND dpsi.step_status            IN( 'IMPLICIT_WAIT','STARTED')
                        AND dpsi.ACTUAL_COMPLETION_DATE IS NULL
        )
UNION ALL
SELECT   dha.source_order_number AS SRC_ORD_NUM,
dha.order_number AS ORDER_NUM,
dha.header_id AS HDR_ID,
        (
                SELECT DISTINCT service_name
                FROM    fusion.DOO_SERVICE_DEFINITIONS_tl
                WHERE   service_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'SVC'
                                        AND language    = userenv('LANG')
                        )
        ) AS Service,
        (
                SELECT DISTINCT display_name
                FROM    fusion.DOO_TASK_INSTANCES sdti,
                        fusion.DOO_TASK_DEFINITIONS_TL sdtt
                WHERE   task_instance_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'TASK'
                                        AND language    = userenv('LANG')
                        )
                        AND sdti.task_id  = sdtt.task_id
                        AND sdtt.language = userenv('LANG')
        ) AS Task             ,
        dmr.REQUEST_FUNCTION AS REQ_FUNC,
        dmr.REQ_ENTITY_TYPE  AS NTT_TYPE,
        dmr.REQUEST_RESULT   AS REQ_RESULT,
        dmb.msg_entity_type  AS MSG_NTT_TYPE,
        dmb.msg_entity_id1   AS MSG_NTT_ID1,
        dmt.message_text     AS MSG_TEXT,
		dmt.creation_Date AS CREATION_DATE
FROM    fusion.DOO_MESSAGE_requests dmr ,
        FUSION.DOO_MESSAGE_ENTITIES DME ,
        fusion.DOO_MESSAGES_B DMB       ,
        fusion.DOO_MESSAGES_TL DMT      ,
        fusion.doo_headers_all dha      ,
        fusion.doo_lines_all dla
WHERE   dmr.MSG_REQUEST_ID       = DMB.MSG_REQUEST_ID
        AND dmr.ACTIVE_FLAG      = 'Y'
        AND DMB.msg_request_id   = DME.msg_request_id
        AND DMB.message_id       = DME.message_id
        AND DMT.message_id       = DMB.message_id
        AND dmt.language         = userenv('LANG')
        AND dmb.MSG_ENTITY_TYPE IN ('SRC_LINE')
        AND dmb.msg_entity_type  = dme.ENTITY_NAME
        AND TO_CHAR(dla.line_id) = dmb.msg_entity_id1
        AND dha.header_id        = dla.header_id
UNION ALL
SELECT   dha.source_order_number AS SRC_ORD_NUM,
dha.order_number AS ORDER_NUM,
dha.header_id AS HDR_ID,
        (
                SELECT DISTINCT service_name
                FROM    fusion.DOO_SERVICE_DEFINITIONS_tl
                WHERE   service_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'SVC'
                                        AND language    = userenv('LANG')
                        )
        ) AS Service,
        (
                SELECT DISTINCT display_name
                FROM    fusion.DOO_TASK_INSTANCES sdti,
                        fusion.DOO_TASK_DEFINITIONS_TL sdtt
                WHERE   task_instance_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'TASK'
                                        AND language    = userenv('LANG')
                        )
                        AND sdti.task_id  = sdtt.task_id
                        AND sdtt.language = userenv('LANG')
        ) AS Task             ,
        dmr.REQUEST_FUNCTION AS REQ_FUNC,
        dmr.REQ_ENTITY_TYPE  AS NTT_TYPE,
        dmr.REQUEST_RESULT   AS REQ_RESULT,
        dmb.msg_entity_type  AS MSG_NTT_TYPE,
        dmb.msg_entity_id1   AS MSG_NTT_ID1,
        dmt.message_text     AS MSG_TEXT,
		dmt.creation_Date AS CREATION_DATE
FROM    fusion.DOO_MESSAGE_requests dmr        ,
        FUSION.DOO_MESSAGE_ENTITIES DME        ,
        fusion.DOO_MESSAGES_B DMB              ,
        fusion.DOO_MESSAGES_TL DMT             ,
        fusion.doo_headers_all dha             ,
        fusion.doo_lines_all dla               ,
        fusion.doo_fulfill_lines_all dfla      ,
        FUSION.doo_ORCHESTRATION_GROUPS DOG    ,
        fusion.DOO_TASK_INSTANCES DTI
WHERE   dmr.MSG_REQUEST_ID                = DMB.MSG_REQUEST_ID
        AND dmr.ACTIVE_FLAG               = 'Y'
        AND DMB.msg_request_id            = DME.msg_request_id
        AND DMB.message_id                = DME.message_id
        AND DMT.message_id                = DMB.message_id
        AND dmt.language                  = userenv('LANG')
        AND dmb.MSG_ENTITY_TYPE          IN ('TASK')
        AND dmb.msg_entity_type           = dme.ENTITY_NAME
        AND TO_CHAR(dti.TASK_INSTANCE_ID) = dmb.msg_entity_id1
        AND dha.header_id                 = dfla.header_id
        AND dfla.line_id                  = dla.line_id
        AND dfla.fulfill_line_id          = dog.fulfillment_line_id
        AND dog.status                    = 'ACTIVE'
        AND dog.DOO_PROCESS_INSTANCE_ID                  = dti.DOO_PROCESS_INSTANCE_ID
UNION ALL
SELECT   dha.source_order_number AS SRC_ORD_NUM,
dha.order_number AS ORDER_NUM,
dha.header_id AS HDR_ID,
        (
                SELECT DISTINCT service_name
                FROM    fusion.DOO_SERVICE_DEFINITIONS_tl
                WHERE   service_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'SVC'
                                        AND language    = userenv('LANG')
                        )
        ) AS Service,
        (
                SELECT DISTINCT display_name
                FROM    fusion.DOO_TASK_INSTANCES sdti,
                        fusion.DOO_TASK_DEFINITIONS_TL sdtt
                WHERE   task_instance_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'TASK'
                                        AND language    = userenv('LANG')
                        )
                        AND sdti.task_id  = sdtt.task_id
                        AND sdtt.language = userenv('LANG')
        ) AS Task             ,
        dmr.REQUEST_FUNCTION AS REQ_FUNC,
        dmr.REQ_ENTITY_TYPE  AS NTT_TYPE,
        dmr.REQUEST_RESULT   AS REQ_RESULT,
        dmb.msg_entity_type  AS MSG_NTT_TYPE,
        dmb.msg_entity_id1   AS MSG_NTT_ID1,
        dmt.message_text     AS MSG_TEXT,
		dmt.creation_Date AS CREATION_DATE
FROM    fusion.DOO_MESSAGE_requests dmr ,
        FUSION.DOO_MESSAGE_ENTITIES DME ,
        fusion.DOO_MESSAGES_B DMB       ,
        fusion.DOO_MESSAGES_TL DMT      ,
        fusion.doo_headers_all dha
WHERE   dmr.MSG_REQUEST_ID         = DMB.MSG_REQUEST_ID
        AND dmr.ACTIVE_FLAG        = 'Y'
        AND DMB.msg_request_id     = DME.msg_request_id
        AND DMB.message_id         = DME.message_id
        AND DMT.message_id         = DMB.message_id
        AND dmt.language           = userenv('LANG')
        AND dmb.MSG_ENTITY_TYPE   IN ('SRC_ORDER','ORDER')
        AND dmb.msg_entity_type    = dme.ENTITY_NAME
        AND TO_CHAR(dha.HEADER_ID) = dmb.msg_entity_id1
UNION ALL
SELECT   dha.source_order_number AS SRC_ORD_NUM,
dha.order_number AS ORDER_NUM,
dha.header_id AS HDR_ID,
        (
                SELECT DISTINCT service_name
                FROM    fusion.DOO_SERVICE_DEFINITIONS_tl
                WHERE   service_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'SVC'
                                        AND language    = userenv('LANG')
                        )
        ) AS Service,
        (
                SELECT DISTINCT display_name
                FROM    fusion.DOO_TASK_INSTANCES sdti,
                       fusion.DOO_TASK_DEFINITIONS_TL sdtt
                WHERE   task_instance_id IN
                        (
                                SELECT  entity_id
                                FROM    Fusion.doo_message_entities
                                WHERE   message_id      = dme.message_id
                                        AND entity_name = 'TASK'
                                        AND language    = userenv('LANG')
                        )
                        AND sdti.task_id  = sdtt.task_id
                        AND sdtt.language = userenv('LANG')
        ) AS Task             ,
        dmr.REQUEST_FUNCTION AS REQ_FUNC,
        dmr.REQ_ENTITY_TYPE  AS NTT_TYPE,
        dmr.REQUEST_RESULT   AS REQ_RESULT,
        dmb.msg_entity_type  AS MSG_NTT_TYPE,
        dmb.msg_entity_id1   AS MSG_NTT_ID1,
        dmt.message_text     AS MSG_TEXT,
		dmt.creation_Date AS CREATION_DATE
FROM    fusion.DOO_MESSAGE_requests dmr   ,
        FUSION.DOO_MESSAGE_ENTITIES DME   ,
        fusion.DOO_MESSAGES_B DMB         ,
        fusion.DOO_MESSAGES_TL DMT        ,
        fusion.doo_headers_all dha        ,
        fusion.doo_lines_all dla          ,
        fusion.doo_fulfill_lines_all dfla ,
        FUSION.doo_ORCHESTRATION_GROUPS DOG
WHERE   dmr.MSG_REQUEST_ID                       = DMB.MSG_REQUEST_ID
        AND dmr.ACTIVE_FLAG                      = 'Y'
        AND DMB.msg_request_id                   = DME.msg_request_id
        AND DMB.message_id                       = DME.message_id
        AND DMT.message_id                       = DMB.message_id
        AND dmt.language                         = userenv('LANG')
        AND dmb.MSG_ENTITY_TYPE                 IN ('PROCESS')
        AND dmb.msg_entity_type                  = dme.ENTITY_NAME
        AND TO_CHAR(dog.DOO_PROCESS_INSTANCE_ID) = dmb.msg_entity_id1
        AND dha.header_id                        = dfla.header_id
        AND dfla.line_id                         = dla.line_id
        AND dfla.fulfill_line_id                 = dog.fulfillment_line_id
        AND dog.status                           = 'ACTIVE'
) 