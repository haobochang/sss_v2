-- create table adj_factor
-- (
--     symbol     varchar(10) not null,
--     `before`   float       not null,
--     after      float       not null,
--     adj_ratio  float       not null,
--     start_date varchar(10) not null,
--     end_date   varchar(10) null
-- );

create table blacklist_broker
(
    id           int auto_increment
        primary key,
    broker_abbr  varchar(255)                          null,
    broker_name  varchar(255)                          null,
    secu_code    varchar(255)                          null,
    secu_abbr    varchar(255)                          null,
    type         varchar(255)                          null,
    open_limit   varchar(255)                          null,
    close_limit  varchar(255)                          null,
    start_date   date                                  null,
    end_date     date                                  null,
    updater      varchar(25) default 'blacklist'       not null,
    updated_time timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx0
    on blacklist_broker (broker_abbr, type, start_date, end_date);

create table blacklist_config
(
    id                     int auto_increment
        primary key,
    fund_code              varchar(255)                          null,
    fund_name              varchar(255)                          null,
    broker_abbr            varchar(255)                          null,
    broker_name            varchar(255)                          null,
    strategy               varchar(255)                          null,
    remark                 varchar(255)                          null,
    blacklist_source_table varchar(255)                          null,
    blacklist_config       varchar(255)                          null,
    priority               int         default 1                 null,
    start_date             date                                  null,
    end_date               date                                  null,
    updater                varchar(25) default 'blacklist'       not null,
    updated_time           timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx_fundcode_date
    on blacklist_config (fund_code, start_date, end_date);

create index idx_remark_date
    on blacklist_config (remark, start_date, end_date);

create table blacklist_globe
(
    id           int auto_increment
        primary key,
    type         varchar(255)                          null,
    secu_code    varchar(255)                          null,
    secu_abbr    varchar(255)                          null,
    `desc`       varchar(255)                          null,
    open_limit   varchar(255)                          null,
    close_limit  varchar(255)                          null,
    start_date   date                                  null,
    end_date     date                                  null,
    updater      varchar(25) default 'blacklist'       not null,
    updated_time timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx0
    on blacklist_globe (type, start_date, end_date);

create table blacklist_investor
(
    id           int auto_increment
        primary key,
    investor     varchar(255)                          null,
    secu_code    varchar(255)                          null,
    secu_abbr    varchar(255)                          null,
    type         varchar(255)                          null,
    open_limit   varchar(255)                          null,
    close_limit  varchar(255)                          null,
    start_date   date                                  null,
    end_date     date                                  null,
    updater      varchar(25) default 'blacklist'       not null,
    updated_time timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx0
    on blacklist_investor (investor, type, start_date, end_date);

create table blacklist_product
(
    id           int auto_increment
        primary key,
    product_name varchar(255)                        not null,
    secu_code    varchar(255)                        not null,
    updated_at   timestamp default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx_remark
    on blacklist_product (product_name);

create table blacklist_result
(
    id           bigint auto_increment
        primary key,
    fund_code    varchar(255)                          null,
    broker_abbr  varchar(255)                          null,
    strategy     varchar(255)                          null,
    remark       varchar(255)                          null,
    secu_code    varchar(255)                          null,
    start_date   date                                  null,
    end_date     date                                  null,
    updater      varchar(25) default 'blacklist'       not null,
    updated_time timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx_blacklist_result_enddate
    on blacklist_result (end_date);

create index idx_blacklist_result_start_date
    on blacklist_result (remark, start_date, end_date);

create index idx_date
    on blacklist_result (start_date, end_date);

create index idx_date_fundcode
    on blacklist_result (fund_code, start_date, end_date);

create table blacklist_special
(
    id           int auto_increment
        primary key,
    secu_code    varchar(255)                          null,
    secu_abbr    varchar(255)                          null,
    type         varchar(255)                          null,
    open_limit   varchar(255)                          null,
    close_limit  varchar(255)                          null,
    start_date   date                                  null,
    end_date     date                                  null,
    updater      varchar(25) default 'blacklist'       not null,
    updated_time timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx0
    on blacklist_special (type, start_date, end_date);

create table blacklist_strategy
(
    id            int auto_increment
        primary key,
    strategy_id   varchar(255)                          null,
    strategy_name varchar(255)                          null,
    secu_code     varchar(255)                          null,
    secu_abbr     varchar(255)                          null,
    type          varchar(255)                          null,
    open_limit    varchar(255)                          null,
    close_limit   varchar(255)                          null,
    start_date    date                                  null,
    end_date      date                                  null,
    updater       varchar(25) default 'blacklist'       not null,
    updated_time  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx0
    on blacklist_strategy (strategy_name, type, start_date, end_date);

create table blacklist_universe
(
    id            int auto_increment
        primary key,
    universe_name varchar(255)                          not null,
    secu_code     varchar(255)                          not null,
    secu_abbr     varchar(255)                          null,
    start_date    date                                  not null,
    end_date      date                                  null,
    updater       varchar(25) default 'blacklist'       not null,
    updated_time  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index idx0_name_date
    on blacklist_universe (universe_name, start_date, end_date);

create index idx1_date
    on blacklist_universe (start_date);

create index idx_end_date
    on blacklist_universe (end_date);

create table bs_algo_cost
(
    id                     int auto_increment
        primary key,
    trading_day            varchar(10)                           not null,
    bs_id                  int                                   not null,
    business               varchar(255)                          null,
    symbol                 varchar(255)                          null,
    type                   int                                   not null,
    weight                 decimal(18, 12)                       not null,
    cost                   decimal(18, 12)                       not null,
    ratio_adjusting_factor decimal(18, 12)                       not null,
    adj_cost               decimal(18, 12)                       not null,
    updater                varchar(25) default 'bs'              not null,
    created_at             timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_algo_cost_index
    on bs_algo_cost (trading_day, bs_id);

create table bs_algo_cost_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_algo_cost_status_index
    on bs_algo_cost_status (trading_day, bs_id);

create table bs_algo_to
(
    id                   int auto_increment
        primary key,
    trading_day          varchar(10)                           not null,
    bs_id                int                                   not null,
    initial_trade_return decimal(18, 12)                       null,
    turnover_fee         decimal(18, 12)                       null,
    turnover_cost        decimal(18, 12)                       null,
    pre_optimal_sumwt    decimal(18, 12)                       null,
    optimal_sumwt        decimal(18, 12)                       null,
    updater              varchar(25) default 'bs'              not null,
    created_at           timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_algo_to_index
    on bs_algo_to (trading_day, bs_id);

create table bs_config
(
    id                   int auto_increment
        primary key,
    bs_id                int                                 not null,
    scheduled_start_time varchar(8)                          null,
    algo_info            varchar(254)                        null,
    start_date           timestamp                           null,
    end_date             timestamp                           null,
    created_time         timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create index bs_config_index
    on bs_config (bs_id, start_date, end_date);

create table bs_info
(
    id                    int                                not null,
    name                  varchar(254)                       not null,
    hedge                 varchar(254)                       not null,
    model                 varchar(254)                       not null,
    sub_model             varchar(254)                       not null,
    size_up_limit         double                             null,
    size_down_limit       double                             null,
    use_alpha_univ        varchar(254)                       not null,
    alpha_cut             double                             not null,
    use_axioma            varchar(254)                       not null,
    max_risk              double                             null,
    risk_aversion         int                                not null,
    cost_aversion         double                             not null,
    universe              varchar(254)                       null,
    universe_type         varchar(254)                       not null,
    universe_weight_min   double                             not null,
    black_list            varchar(254)                       not null,
    limit_symbols         varchar(254)                       not null,
    nobuy_symbols         varchar(254)                       not null,
    nosell_symbols        varchar(254)                       not null,
    sell_symbols          varchar(254)                       not null,
    max_weight            double                             not null,
    symbols_max_wt        varchar(254)                       null,
    if_liquid             varchar(254)                       not null,
    target_amount         bigint                             null,
    top_float             double                             not null,
    float_trade           double                             null,
    float_cut             double                             null,
    if_xs                 varchar(254)                       not null,
    limit_day             int                                not null,
    industry_up_limit     varchar(254)                       null,
    industry_down_limit   varchar(254)                       null,
    style_up_limit        varchar(254)                       null,
    style_down_limit      varchar(254)                       null,
    size_cut              double                             null,
    shift_alpha           varchar(254)                       not null,
    turnover_rate         double                             not null,
    specific_ind_exp_up   varchar(254)                       null,
    specific_ind_exp_down varchar(254)                       null,
    specific_ind          varchar(254)                       null,
    weight_bias           varchar(254)                       null,
    benchmark_weight_min  double                             not null,
    fill_alpha_na         varchar(254)                       not null,
    use_updown_limit      varchar(254)                       not null,
    start_date            datetime                           null,
    end_date              datetime                           null,
    created_at            datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create index bs_info_index
    on bs_info (id, start_date, end_date);

create table bs_info_id_of_sp
(
    id         int auto_increment comment '基准策略id'
        primary key,
    sp_id      int                                    not null comment '策略池中bs_id',
    sp_version varchar(255)                           not null comment '策略池版本',
    updater    varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at datetime     default CURRENT_TIMESTAMP not null comment '插入时写入，如不指定，默认值为插入时时间',
    updated_at datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '插入和更新时写入，如不指定，默认值为更新时间'
)
    comment '该表用来记录策略池中的基准策略的id,model,strategy,algo等信息';

create table bs_info_test
(
    id                    int                                not null,
    name                  varchar(254)                       not null,
    hedge                 varchar(254)                       not null,
    model                 varchar(254)                       not null,
    sub_model             varchar(254)                       not null,
    size_up_limit         double                             null,
    size_down_limit       double                             null,
    use_alpha_univ        varchar(254)                       not null,
    alpha_cut             double                             not null,
    use_axioma            varchar(254)                       not null,
    max_risk              double                             null,
    risk_aversion         int                                not null,
    cost_aversion         double                             not null,
    universe              varchar(254)                       null,
    universe_type         varchar(254)                       not null,
    universe_weight_min   double                             not null,
    black_list            varchar(254)                       not null,
    limit_symbols         varchar(254)                       not null,
    nobuy_symbols         varchar(254)                       not null,
    nosell_symbols        varchar(254)                       not null,
    sell_symbols          varchar(254)                       not null,
    max_weight            double                             not null,
    symbols_max_wt        varchar(254)                       null,
    if_liquid             varchar(254)                       not null,
    target_amount         bigint                             null,
    top_float             double                             not null,
    float_trade           double                             null,
    float_cut             double                             null,
    if_xs                 varchar(254)                       not null,
    limit_day             int                                not null,
    industry_up_limit     varchar(254)                       null,
    industry_down_limit   varchar(254)                       null,
    style_up_limit        varchar(254)                       null,
    style_down_limit      varchar(254)                       null,
    size_cut              double                             null,
    shift_alpha           varchar(254)                       not null,
    turnover_rate         double                             not null,
    specific_ind_exp_up   varchar(254)                       null,
    specific_ind_exp_down varchar(254)                       null,
    specific_ind          varchar(254)                       null,
    weight_bias           varchar(254)                       null,
    benchmark_weight_min  double                             not null,
    fill_alpha_na         varchar(254)                       not null,
    use_updown_limit      varchar(254)                       not null,
    start_date            datetime                           null,
    end_date              datetime                           null,
    created_at            datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create index bs_info_index
    on bs_info_test (id, start_date, end_date);

create table bs_info_v2
(
    id                        int auto_increment
        primary key,
    bs_id                     int                                              not null comment '基准策略id',
    name                      varchar(255)                                     not null,
    model                     varchar(255)                                     not null,
    sub_model                 varchar(255)                                     not null,
    initial_position          varchar(255) default 'None'                      not null comment '内容：empty/sp/mannual',
    symbols_max_wt            varchar(255) default 'None'                      not null,
    from_date                 varchar(255)                                     not null,
    to_date                   varchar(255)                                     null,
    frequency                 varchar(255) default '1'                         not null,
    use_time                  varchar(255) default '1000_1030'                 not null,
    trade_time                varchar(255) default '1000_1030'                 not null,
    benchmark                 varchar(255) default '000905'                    not null,
    alpha_preprocess          varchar(255) default 'True'                      not null,
    shift_alpha               varchar(255) default 'False'                     not null,
    alpha_cut                 varchar(255) default '1'                         not null,
    size_cut                  varchar(255) default '1'                         not null,
    price_cut                 varchar(255)                                     not null,
    listed_dates_num_cut      varchar(255)                                     not null,
    black_list                varchar(255) default '[]'                        not null,
    nobuy_symbols             varchar(255) default '[]'                        not null,
    nosell_symbols            varchar(255) default '[]'                        not null,
    sell_symbols              varchar(255) default '[]'                        not null,
    max_weight                varchar(255) default '0'                         not null,
    weight_bias               varchar(255) default '[]'                        not null,
    if_liquid                 varchar(255) default 'True'                      not null,
    universe_type             varchar(255) default 'None'                      not null,
    universe                  varchar(255) default '[]'                        not null,
    universe_weight_min       varchar(255) default '1'                         not null,
    benchmark_weight_min      varchar(255) default '0'                         not null,
    style_up_limit            varchar(255) default 'None'                      not null,
    style_down_limit          varchar(255) default 'None'                      not null,
    size_up_limit             varchar(255) default 'None'                      not null,
    size_down_limit           varchar(255) default 'None'                      not null,
    industry_up_limit         varchar(255) default '0.05'                      not null,
    industry_down_limit       varchar(255) default '-0.05'                     not null,
    specific_ind              varchar(255) default '[]'                        not null,
    specific_ind_exp_up       varchar(255) default '[]'                        not null,
    specific_ind_exp_down     varchar(255) default '[]'                        not null,
    second_ind                varchar(255) default '[]'                        not null,
    second_ind_exp_up         varchar(255) default '[]'                        not null,
    second_ind_exp_down       varchar(255) default '[]'                        not null,
    turnover_rate             varchar(255) default '0'                         not null,
    risk_aversion             varchar(255) default '0'                         not null,
    cost_aversion             varchar(255) default '0'                         not null,
    max_risk                  varchar(255) default 'None'                      not null,
    use_axioma                varchar(255) default 'False'                     not null,
    comms_slippange_stampduty varchar(255) default '[0.00035, 0.00115, 0.001]' not null,
    aum                       varchar(255)                                     not null,
    index_aum                 varchar(255)                                     not null,
    max_liq_awv               varchar(255)                                     not null,
    awv_cut                   varchar(255)                                     not null,
    extra_constraints         varchar(255)                                     not null,
    dynamic_param             varchar(1024)                                    not null,
    extra_industry_limit      varchar(512)                                     not null,
    float_cap_limit           varchar(255)                                     not null,
    listed_sector_limit       varchar(255)                                     null,
    created_at                datetime     default CURRENT_TIMESTAMP           not null comment '插入时写入，如不指定，默认值为插入时时间',
    updated_at                datetime     default CURRENT_TIMESTAMP           not null on update CURRENT_TIMESTAMP comment '插入和更新时写入，如不指定，默认值为更新时间',
    status                    tinyint      default 1                           not null comment '是否启用：0-否，1-是, -1 未知',
    updater                   varchar(255) default ''                          null comment '更新者，可作为修改批次号'
)
    comment '该表用来记录策略池中的基准策略的id,model,strategy,algo等信息';

create table bs_info_v2_detail
(
    id                        int auto_increment
        primary key,
    trading_day               date                                             null,
    bs_id                     int                                              not null comment '基准策略id',
    name                      varchar(255)                                     not null,
    model                     varchar(255)                                     not null,
    sub_model                 varchar(255)                                     not null,
    initial_position          varchar(255) default 'None'                      not null comment '内容：empty/sp/mannual',
    symbols_max_wt            varchar(255) default 'None'                      not null,
    from_date                 varchar(255)                                     not null,
    to_date                   varchar(255)                                     null,
    frequency                 varchar(255) default '1'                         not null,
    use_time                  varchar(255) default '1000_1030'                 not null,
    trade_time                varchar(255) default '1000_1030'                 not null,
    benchmark                 varchar(255) default '000905'                    not null,
    alpha_preprocess          varchar(255) default 'True'                      not null,
    shift_alpha               varchar(255) default 'False'                     not null,
    alpha_cut                 varchar(255) default '1'                         not null,
    size_cut                  varchar(255) default '1'                         not null,
    price_cut                 varchar(255)                                     not null,
    listed_dates_num_cut      varchar(255)                                     not null,
    black_list                varchar(255) default '[]'                        not null,
    nobuy_symbols             varchar(255) default '[]'                        not null,
    nosell_symbols            varchar(255) default '[]'                        not null,
    sell_symbols              varchar(255) default '[]'                        not null,
    max_weight                varchar(255) default '0'                         not null,
    weight_bias               varchar(255) default '[]'                        not null,
    if_liquid                 varchar(255) default 'True'                      not null,
    universe_type             varchar(255) default 'None'                      not null,
    universe                  varchar(255) default '[]'                        not null,
    universe_weight_min       varchar(255) default '1'                         not null,
    benchmark_weight_min      varchar(255) default '0'                         not null,
    style_up_limit            varchar(255) default 'None'                      not null,
    style_down_limit          varchar(255) default 'None'                      not null,
    size_up_limit             varchar(255) default 'None'                      not null,
    size_down_limit           varchar(255) default 'None'                      not null,
    industry_up_limit         varchar(255) default '0.05'                      not null,
    industry_down_limit       varchar(255) default '-0.05'                     not null,
    specific_ind              varchar(255) default '[]'                        not null,
    specific_ind_exp_up       varchar(255) default '[]'                        not null,
    specific_ind_exp_down     varchar(255) default '[]'                        not null,
    second_ind                varchar(255) default '[]'                        not null,
    second_ind_exp_up         varchar(255) default '[]'                        not null,
    second_ind_exp_down       varchar(255) default '[]'                        not null,
    turnover_rate             varchar(255) default '0'                         not null,
    risk_aversion             varchar(255) default '0'                         not null,
    cost_aversion             varchar(255) default '0'                         not null,
    max_risk                  varchar(255) default 'None'                      not null,
    use_axioma                varchar(255) default 'False'                     not null,
    comms_slippange_stampduty varchar(255) default '[0.00035, 0.00115, 0.001]' not null,
    aum                       varchar(255)                                     not null,
    index_aum                 varchar(255)                                     not null,
    max_liq_awv               varchar(255)                                     not null,
    awv_cut                   varchar(255)                                     not null,
    extra_constraints         varchar(255)                                     not null,
    dynamic_param             varchar(1024)                                    not null,
    extra_industry_limit      varchar(512)                                     not null,
    float_cap_limit           varchar(255)                                     not null,
    opt_type                  int          default 1                           not null comment '1 alpha优化；2 优化前填充',
    listed_sector_limit       varchar(255)                                     null,
    turnover_rate_initial     varchar(128)                                     null,
    force_in_universe         varchar(128) default 'False'                     null,
    created_at                datetime     default CURRENT_TIMESTAMP           not null comment '插入时写入，如不指定，默认值为插入时时间',
    updated_at                datetime     default CURRENT_TIMESTAMP           not null on update CURRENT_TIMESTAMP comment '插入和更新时写入，如不指定，默认值为更新时间',
    updater                   varchar(255) default ''                          null comment '更新者，可作为修改批次号'
)
    comment '该表用来记录策略池中的基准策略的id,model,strategy,algo等信息';

create index idx0
    on bs_info_v2_detail (trading_day, bs_id);

create table bs_info_v2_snp
(
    id                        int auto_increment
        primary key,
    trading_day               date                                             null,
    bs_id                     int                                              not null comment '基准策略id',
    name                      varchar(255)                                     not null,
    model                     varchar(255)                                     not null,
    sub_model                 varchar(255)                                     not null,
    initial_position          varchar(255) default 'None'                      not null comment '内容：empty/sp/mannual',
    symbols_max_wt            varchar(255) default 'None'                      not null,
    from_date                 varchar(255)                                     not null,
    to_date                   varchar(255)                                     null,
    frequency                 varchar(255) default '1'                         not null,
    use_time                  varchar(255) default '1000_1030'                 not null,
    trade_time                varchar(255) default '1000_1030'                 not null,
    benchmark                 varchar(255) default '000905'                    not null,
    alpha_preprocess          varchar(255) default 'True'                      not null,
    shift_alpha               varchar(255) default 'False'                     not null,
    alpha_cut                 varchar(255) default '1'                         not null,
    size_cut                  varchar(255) default '1'                         not null,
    price_cut                 varchar(255)                                     not null,
    listed_dates_num_cut      varchar(255)                                     not null,
    black_list                varchar(255) default '[]'                        not null,
    nobuy_symbols             varchar(255) default '[]'                        not null,
    nosell_symbols            varchar(255) default '[]'                        not null,
    sell_symbols              varchar(255) default '[]'                        not null,
    max_weight                varchar(255) default '0'                         not null,
    weight_bias               varchar(255) default '[]'                        not null,
    if_liquid                 varchar(255) default 'True'                      not null,
    universe_type             varchar(255) default 'None'                      not null,
    universe                  varchar(255) default '[]'                        not null,
    universe_weight_min       varchar(255) default '1'                         not null,
    benchmark_weight_min      varchar(255) default '0'                         not null,
    style_up_limit            varchar(255) default 'None'                      not null,
    style_down_limit          varchar(255) default 'None'                      not null,
    size_up_limit             varchar(255) default 'None'                      not null,
    size_down_limit           varchar(255) default 'None'                      not null,
    industry_up_limit         varchar(255) default '0.05'                      not null,
    industry_down_limit       varchar(255) default '-0.05'                     not null,
    specific_ind              varchar(255) default '[]'                        not null,
    specific_ind_exp_up       varchar(255) default '[]'                        not null,
    specific_ind_exp_down     varchar(255) default '[]'                        not null,
    second_ind                varchar(255) default '[]'                        not null,
    second_ind_exp_up         varchar(255) default '[]'                        not null,
    second_ind_exp_down       varchar(255) default '[]'                        not null,
    turnover_rate             varchar(255) default '0'                         not null,
    risk_aversion             varchar(255) default '0'                         not null,
    cost_aversion             varchar(255) default '0'                         not null,
    max_risk                  varchar(255) default 'None'                      not null,
    use_axioma                varchar(255) default 'False'                     not null,
    comms_slippange_stampduty varchar(255) default '[0.00035, 0.00115, 0.001]' not null,
    aum                       varchar(255)                                     not null,
    index_aum                 varchar(255)                                     not null,
    max_liq_awv               varchar(255)                                     not null,
    awv_cut                   varchar(255)                                     not null,
    extra_constraints         varchar(255)                                     not null,
    dynamic_param             varchar(1024)                                    not null,
    extra_industry_limit      varchar(512)                                     not null,
    float_cap_limit           varchar(255)                                     not null,
    listed_sector_limit       varchar(255)                                     null,
    created_at                datetime     default CURRENT_TIMESTAMP           not null comment '插入时写入，如不指定，默认值为插入时时间',
    updated_at                datetime     default CURRENT_TIMESTAMP           not null on update CURRENT_TIMESTAMP comment '插入和更新时写入，如不指定，默认值为更新时间',
    updater                   varchar(255) default ''                          null comment '更新者，可作为修改批次号'
)
    comment '该表用来记录策略池中的基准策略的id,model,strategy,algo等信息';

create index idx0
    on bs_info_v2_snp (trading_day, bs_id);

create table bs_info_v3
(
    id         int auto_increment
        primary key,
    bs_id      int                                not null,
    name       varchar(254)                       not null,
    hedge      varchar(254)                       not null,
    model      varchar(254)                       not null,
    sub_model  varchar(255)                       null,
    start_date datetime                           null,
    end_date   datetime                           null,
    created_at datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create index bs_info_index
    on bs_info_v3 (id, start_date, end_date);

create table bs_info_v4
(
    id                        int auto_increment
        primary key,
    bs_id                     int                                              not null comment '基准策略id',
    name                      varchar(255)                                     not null,
    model                     varchar(255)                                     not null,
    sub_model                 varchar(255)                                     not null,
    initial_position          varchar(255) default 'None'                      not null comment '内容：empty/sp/mannual',
    from_date                 varchar(255)                                     not null,
    to_date                   varchar(255) default ''                          null,
    frequency                 varchar(255) default '1'                         not null,
    use_time                  varchar(255) default '1000_1030'                 not null,
    trade_time                varchar(255) default '1000_1030'                 not null,
    alpha_preprocess          varchar(255) default 'True'                      not null,
    shift_alpha               varchar(255) default 'False'                     not null,
    alpha_cut                 varchar(255) default '1'                         not null,
    size_cut                  varchar(255) default '1'                         not null,
    price_cut                 varchar(255)                                     not null,
    listed_dates_num_cut      varchar(255)                                     not null,
    black_list_type           varchar(255) default '[]'                        not null,
    long_no_open_symbols      varchar(255) default '[]'                        not null,
    long_no_close_symbols     varchar(255) default '[]'                        not null,
    short_no_open_symbols     varchar(255) default '[]'                        not null,
    short_no_close_symbols    varchar(255) default '[]'                        not null,
    long_force_close_symbols  varchar(255) default '[]'                        not null,
    short_force_close_symbols varchar(255) default '[]'                        not null,
    short_broker_type         varchar(255) default '[]'                        not null,
    long_max_weight           varchar(255) default '0'                         not null,
    short_max_weight          varchar(255) default '0'                         not null,
    long_symbols_max_wt       varchar(255)                                     not null,
    short_symbols_max_wt      varchar(255)                                     not null,
    long_universe_type        varchar(255) default 'None'                      not null,
    long_universe             varchar(255) default '[]'                        not null,
    short_universe_type       varchar(255) default 'None'                      not null,
    short_universe            varchar(255) default '[]'                        not null,
    if_liquid                 varchar(255) default 'True'                      not null,
    aum                       varchar(255)                                     not null,
    max_liq_awv               varchar(255)                                     not null,
    awv_cut                   varchar(255)                                     not null,
    short_max_liq_awv         varchar(255)                                     not null,
    long_universe_weight_min  varchar(255) default '0'                         not null,
    short_universe_weight_min varchar(255) default '0'                         not null,
    style_up_limit            varchar(255) default 'None'                      not null,
    style_down_limit          varchar(255) default 'None'                      not null,
    size_up_limit             varchar(255) default 'None'                      not null,
    size_down_limit           varchar(255) default 'None'                      not null,
    industry_up_limit         varchar(255) default '0.05'                      not null,
    industry_down_limit       varchar(255) default '-0.05'                     not null,
    specific_ind              varchar(255) default '[]'                        not null,
    specific_ind_exp_up       varchar(255) default '[]'                        not null,
    specific_ind_exp_down     varchar(255) default '[]'                        not null,
    second_ind                varchar(255) default '[]'                        not null,
    second_ind_exp_up         varchar(255) default '[]'                        not null,
    second_ind_exp_down       varchar(255) default '[]'                        not null,
    turnover_rate             varchar(255) default '0'                         not null,
    risk_aversion             varchar(255) default '0'                         not null,
    cost_aversion             varchar(255) default '0'                         not null,
    max_risk                  varchar(255) default 'None'                      not null,
    comms_slippange_stampduty varchar(255) default '[0.00035, 0.00115, 0.001]' not null,
    created_at                datetime     default CURRENT_TIMESTAMP           not null comment '插入时写入，如不指定，默认值为插入时时间',
    updated_at                datetime     default CURRENT_TIMESTAMP           not null on update CURRENT_TIMESTAMP comment '插入和更新时写入，如不指定，默认值为更新时间'
)
    comment '该表用来记录策略池中的基准策略的id,model,strategy,algo等信息';

create table bs_nav
(
    id             int auto_increment
        primary key,
    trading_day    varchar(10)                           not null,
    bs_id          int                                   not null,
    minute         varchar(8)                            not null,
    min_weight     decimal(18, 12)                       null,
    nav_adj_factor decimal(18, 12)                       null,
    nav            decimal(18, 12)                       null,
    updater        varchar(25) default 'bs'              not null,
    created_at     timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_nav_index
    on bs_nav (trading_day, bs_id, minute);

create table bs_nav_adj
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    adj_ret     decimal(18, 6)                        null,
    remark      varchar(128)                          null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_nav_index
    on bs_nav_adj (trading_day, bs_id);

create table bs_opt_pos
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    business    varchar(255)                          null,
    symbol      varchar(255)                          null,
    type        int                                   not null,
    weight      decimal(18, 6)                        not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_opt_pos_index
    on bs_opt_pos (trading_day, bs_id);

create table bs_opt_pos_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_opt_pos_status_index
    on bs_opt_pos_status (trading_day, bs_id);

create table bs_opt_pre_pos
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    business    varchar(255)                          null,
    symbol      varchar(10)                           null,
    type        int                                   not null,
    weight      decimal(18, 12)                       not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_opt_pre_pos_index
    on bs_opt_pre_pos (trading_day, bs_id);

create table bs_opt_pre_pos_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_opt_pre_pos_status_index
    on bs_opt_pre_pos_status (trading_day, bs_id);

create table bs_opt_result
(
    id            int auto_increment
        primary key,
    trading_day   varchar(10)                           not null,
    bs_id         int                                   not null,
    status        int                                   not null comment '除200外是原值，200会根据优化结果存0和1，只有0是正常结果',
    turnover_rate float                                 null,
    error_msg     varchar(3000)                         null,
    constraints   varchar(3000)                         null,
    updater       varchar(25) default 'bs'              not null,
    created_at    timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_ret_index
    on bs_opt_result (trading_day, bs_id);

create table bs_pos
(
    id          bigint auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    minute      varchar(8)                            not null,
    business    varchar(255)                          null,
    symbol      varchar(255)                          null,
    type        int                                   not null,
    weight      decimal(18, 12)                       not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_pos_index
    on bs_pos (trading_day, bs_id, minute);

create index bs_pos_tradingday
    on bs_pos (trading_day);

create index idx_bs_pos_minute
    on bs_pos (minute);

create table bs_pos_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    minute      time                                  not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_pos_status_index
    on bs_pos_status (trading_day, bs_id, minute);

create table bs_ret_unuse
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    period varchar (17) not null,
    ret         decimal(18, 6)                        not null,
    index_ret   decimal(18, 6)                        null,
    excess_ret  decimal(18, 6)                        null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_ret_index
    on bs_ret_unuse (trading_day, bs_id, period);

create table bs_summary
(
    id           bigint auto_increment
        primary key,
    trading_day  date                               not null,
    bs_id        bigint                             not null,
    bs_name      varchar(254)                       not null,
    model        varchar(255)                       null,
    sub_model    varchar(255)                       null,
    sp_version   varchar(255)                       not null,
    bspbase_id   bigint                             null,
    bspbase_name varchar(254)                       null,
    optarg_id    bigint                             null,
    optarg_name  varchar(255)                       null,
    model_id     bigint                             null,
    sp_bs_id     bigint                             null,
    created_at   datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create index bs_info_index
    on bs_summary (id);

create index idx_bsid
    on bs_summary (bs_id);

create table bsp_model_to_20241111
(
    bspbase_name varchar(255) null,
    model        varchar(255) null,
    target_wt    varchar(255) null,
    `to`         varchar(255) null
);

create table bsp_pos
(
    id          bigint auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bsp_id      int                                   not null,
    minute      varchar(8)                            not null,
    business    varchar(255)                          null,
    symbol      varchar(255)                          null,
    type        int                                   not null,
    weight      decimal(18, 6)                        not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_pos_index
    on bsp_pos (trading_day, bsp_id, minute);

create table bsp_pos_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bsp_id      int                                   not null,
    minute      time                                  not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_pos_status_index
    on bsp_pos_status (trading_day, bsp_id, minute);

create table bspool_info
(
    id                        int auto_increment comment '基准策略id'
        primary key,
    name                      varchar(255)                                     not null,
    model                     varchar(255)                                     not null,
    sub_model                 varchar(255)                                     not null,
    latest_opt_wt             varchar(255) default 'None'                      not null,
    initial_position          varchar(255) default 'None'                      not null,
    symbols_max_wt            varchar(255) default 'None'                      not null,
    backtest_type             varchar(255) default 'opt_ret'                   not null,
    from_date                 varchar(255)                                     not null,
    to_date                   varchar(255)                                     null,
    frequency                 varchar(255) default '1'                         not null,
    use_time                  varchar(255) default '1000_1030'                 not null,
    trade_time                varchar(255) default '1000_1030'                 not null,
    `index`                   varchar(255) default '000905'                    not null,
    alpha_preprocess          varchar(255) default 'True'                      not null,
    shift_alpha               varchar(255) default 'False'                     not null,
    universe_type             varchar(255) default 'None'                      not null,
    universe                  varchar(255) default '[]'                        not null,
    alpha_cut                 varchar(255) default '1'                         not null,
    size_cut                  varchar(255) default '1'                         not null,
    price_cut                 varchar(255)                                     not null,
    listed_dates_num_cut      varchar(255)                                     not null,
    float_cut                 varchar(255) default '1'                         not null,
    if_xs                     varchar(255) default 'False'                     not null,
    xs_limit_days             varchar(255) default '60'                        not null,
    black_list                varchar(255) default '[]'                        not null,
    nobuy_symbols             varchar(255) default '[]'                        not null,
    max_weight                varchar(255) default '0'                         not null,
    weight_bias               varchar(255) default '[]'                        not null,
    if_liquid                 varchar(255) default 'True'                      not null,
    target_amount             varchar(255) default 'None'                      not null,
    top_float                 varchar(255) default '0.1'                       not null,
    float_trade               varchar(255) default 'None'                      not null,
    nosell_symbols            varchar(255) default '[]'                        not null,
    sell_symbols              varchar(255) default '[]'                        not null,
    universe_weight_min       varchar(255) default '1'                         not null,
    benchmark_weight_min      varchar(255) default '0'                         not null,
    style_up_limit            varchar(255) default 'None'                      not null,
    style_down_limit          varchar(255) default 'None'                      not null,
    size_up_limit             varchar(255) default 'None'                      not null,
    size_down_limit           varchar(255) default 'None'                      not null,
    industry_up_limit         varchar(255) default '0.05'                      not null,
    industry_down_limit       varchar(255) default '-0.05'                     not null,
    specific_ind              varchar(255) default '[]'                        not null,
    specific_ind_exp_up       varchar(255) default '[]'                        not null,
    specific_ind_exp_down     varchar(255) default '[]'                        not null,
    second_ind                varchar(255) default '[]'                        not null,
    second_ind_exp_up         varchar(255) default '[]'                        not null,
    second_ind_exp_down       varchar(255) default '[]'                        not null,
    turnover_rate             varchar(255) default '0'                         not null,
    risk_aversion             varchar(255) default '0'                         not null,
    cost_aversion             varchar(255) default '0'                         not null,
    max_risk                  varchar(255) default 'None'                      not null,
    use_axioma                varchar(255) default 'False'                     not null,
    lag_days                  varchar(255) default '[-240,20]'                 not null,
    comms_slippange_stampduty varchar(255) default '[0.00035, 0.00115, 0.001]' not null,
    created_at                datetime     default CURRENT_TIMESTAMP           not null comment '插入时写入，如不指定，默认值为插入时时间',
    updated_at                datetime     default CURRENT_TIMESTAMP           not null on update CURRENT_TIMESTAMP comment '插入和更新时写入，如不指定，默认值为更新时间'
)
    comment '该表用来记录策略池中的基准策略的id,model,strategy,algo等信息';

create table cfg_basis_pos_pct
(
    id            bigint auto_increment
        primary key,
    fund_id       bigint                                not null comment '基金id',
    basis_type    varchar(255)                          null comment '300/500/1000指增、300/500/1000对冲、灵活对冲',
    is_id         int                                   not null,
    basis_pos_pct double                                not null comment '基差仓位',
    start_date    date                                  not null,
    end_date      date                                  null,
    start_time    time                                  null,
    end_time      time                                  null,
    updater       varchar(50) default ''                null comment '更新者，可作为修改批次号',
    created_at    datetime    default CURRENT_TIMESTAMP null,
    updated_at    datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create index idx_fund_id
    on cfg_basis_pos_pct (fund_id);

create table cfg_fund_is
(
    id         bigint auto_increment
        primary key,
    fund_id    int                                    not null,
    is_id      int                                    not null,
    wt         double                                 not null,
    start_date date                                   not null,
    end_date   date                                   null,
    start_time time                                   null,
    end_time   time                                   null,
    updater    varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at datetime     default CURRENT_TIMESTAMP null,
    updated_at datetime     default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    src_is_id  int                                    null comment '针对变更is_bsp的场景，记录变更来源'
);

create index idx_fund_is
    on cfg_fund_is (fund_id, is_id);

create index is_id
    on cfg_fund_is (is_id);

create table cfg_is_bsp
(
    id         bigint auto_increment
        primary key,
    is_id      int                                    not null,
    bsp_id     int                                    not null,
    wt         double                                 not null,
    start_date date                                   not null,
    end_date   date                                   null,
    start_time time                                   null,
    end_time   time                                   null,
    updater    varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at datetime     default CURRENT_TIMESTAMP null,
    updated_at datetime     default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create index idx_is_bsp
    on cfg_is_bsp (is_id, bsp_id);

create table cfg_is_bsp_copy1
(
    id         bigint auto_increment
        primary key,
    is_id      int                                    not null,
    bsp_id     int                                    not null,
    wt         double                                 not null,
    start_date date                                   not null,
    end_date   date                                   null,
    start_time time                                   null,
    end_time   time                                   null,
    updater    varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at datetime     default CURRENT_TIMESTAMP null,
    updated_at datetime     default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create index idx_is_bsp
    on cfg_is_bsp_copy1 (is_id, bsp_id);

create table fund_snapshot
(
    id             bigint auto_increment
        primary key,
    fund_id        bigint                                not null comment '基金id',
    fund_asset     decimal(18, 6)                        not null comment '基金产品资产',
    is_id          bigint                                not null comment '投资策略id',
    is_name        varchar(255)                          not null comment '投资策略名称',
    is_type        varchar(255)                          not null,
    bsp_id         bigint                                null comment '基准组合id',
    bsp_name       varchar(255)                          null comment '基准组合名称',
    bsp_type       varchar(255)                          null comment 'stock|future',
    sa_type        varchar(255)                          null comment '策略账户类型',
    is_wt          double                                not null comment '投资策略权重',
    bsp_wt         double                                null comment '基准组合权重',
    basis_pos_pct  double                                null comment '基差仓位',
    mv_wt          double                                null comment '目标市值权重',
    bsp_asset      decimal(18, 6)                        null,
    bsp_mv         double                                null,
    bsp_share      int                                   null comment '期货手数',
    future_price   double                                null comment '期货价格',
    target_is_expo double                                null comment '目标is expo',
    trading_day    date                                  not null comment '交易日',
    updater        varchar(50) default ''                null comment '更新者，可作为修改批次号',
    created_at     datetime    default CURRENT_TIMESTAMP null,
    updated_at     datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create index idx_fund_id
    on fund_snapshot (fund_id);

create index idx_trading_day
    on fund_snapshot (trading_day);

create table future_bs_algo_cost
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    business    varchar(32)                           null,
    symbol      varchar(32)                           null,
    type        int                                   not null,
    weight      decimal(18, 12)                       not null,
    cost        decimal(18, 12)                       not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_algo_cost_index
    on future_bs_algo_cost (trading_day, bs_id);

create table future_bs_algo_cost_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_algo_cost_status_index
    on future_bs_algo_cost_status (trading_day, bs_id);

create table future_bs_info
(
    id         int auto_increment
        primary key,
    bs_id      int                                    not null comment '基准策略id',
    name       varchar(255)                           not null,
    model      varchar(255) default 'True'            not null,
    benchmark  varchar(255) default '000905'          not null,
    type       varchar(255)                           not null,
    trade_time varchar(255)                           not null,
    from_date  varchar(255)                           not null,
    to_date    varchar(255)                           null,
    created_at datetime     default CURRENT_TIMESTAMP not null comment '插入时写入，如不指定，默认值为插入时时间',
    updated_at datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '插入和更新时写入，如不指定，默认值为更新时间'
)
    comment '该表用来记录策略池中的基准策略的id,model,strategy,algo等信息';

create index idx0
    on future_bs_info (bs_id);

create table future_bs_info_snp
(
    id          int auto_increment
        primary key,
    bs_id       int                                    not null comment '基准策略id',
    name        varchar(255)                           not null,
    model       varchar(255) default 'True'            not null,
    benchmark   varchar(255) default '000905'          not null,
    type        varchar(255)                           not null,
    trade_time  varchar(255)                           not null,
    from_date   varchar(255)                           not null,
    to_date     varchar(255)                           null,
    opt_type    int          default 1                 not null,
    trading_day date                                   not null,
    created_at  datetime     default CURRENT_TIMESTAMP not null comment '插入时写入，如不指定，默认值为插入时时间',
    updated_at  datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '插入和更新时写入，如不指定，默认值为更新时间'
)
    comment '该表用来记录策略池中的基准策略的id,model,strategy,algo等信息';

create index idx0
    on future_bs_info_snp (bs_id);

create table future_bs_opt_pos
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    business    varchar(255)                          null,
    symbol      varchar(255)                          null,
    type        int                                   not null,
    weight      decimal(18, 6)                        not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_opt_pos_index
    on future_bs_opt_pos (trading_day, bs_id);

create table future_bs_opt_pos_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_opt_pos_status_index
    on future_bs_opt_pos_status (trading_day, bs_id);

create table future_bs_opt_pre_pos
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    business    varchar(255)                          null,
    symbol      varchar(32)                           null,
    type        int                                   not null,
    weight      decimal(18, 12)                       not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_opt_pre_pos_index
    on future_bs_opt_pre_pos (trading_day, bs_id);

create table future_bs_opt_pre_pos_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_opt_pre_pos_status_index
    on future_bs_opt_pre_pos_status (trading_day, bs_id);

create table future_bs_opt_result
(
    id            int auto_increment
        primary key,
    trading_day   varchar(10)                           not null,
    bs_id         int                                   not null,
    status        int                                   not null comment '除200外是原值，200会根据优化结果存0和1，只有0是正常结果',
    turnover_rate float                                 null,
    error_msg     varchar(3000)                         null,
    other_msg     varchar(3000)                         null,
    updater       varchar(25) default 'bs'              not null,
    created_at    timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_ret_index
    on future_bs_opt_result (trading_day, bs_id);

create table future_bs_pos
(
    id          bigint auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    minute      varchar(8)                            not null,
    business    varchar(255)                          null,
    symbol      varchar(255)                          null,
    type        int                                   not null,
    weight      decimal(18, 12)                       not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_pos_index
    on future_bs_pos (trading_day, bs_id, minute);

create index bs_pos_tradingday
    on future_bs_pos (trading_day);

create index idx_bs_pos_minute
    on future_bs_pos (minute);

create table future_bs_pos_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bs_id       int                                   not null,
    minute      varchar(8)                            not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_pos_status_index
    on future_bs_pos_status (trading_day, bs_id, minute);

create table future_bsp_detail
(
    id         int auto_increment
        primary key,
    bsp_id     int                                not null,
    bs_id      int                                not null,
    wt         double                             not null,
    start_date date                               not null,
    end_date   date                               null,
    updated_at datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create index idx_0
    on future_bsp_detail (bsp_id, bs_id);

create table future_bsp_detail_snp
(
    id          int auto_increment
        primary key,
    bsp_id      int                                not null,
    bs_id       int                                not null,
    wt          double                             not null,
    trading_day date                               not null,
    updated_at  datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create index idx_0
    on future_bsp_detail_snp (bsp_id, bs_id);

create table future_bsp_pos
(
    id          bigint auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bsp_id      int                                   not null,
    minute      varchar(8)                            not null,
    business    varchar(255)                          null,
    symbol      varchar(255)                          null,
    type        int                                   not null,
    weight      decimal(18, 6)                        not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_pos_index
    on future_bsp_pos (trading_day, bsp_id, minute);

create table future_bsp_pos_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    bsp_id      int                                   not null,
    minute      varchar(8)                            not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index bs_pos_status_index
    on future_bsp_pos_status (trading_day, bsp_id, minute);

create table future_fund_bsp_share
(
    id          bigint auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    fund_id     int                                   not null,
    bsp_id      int                                   not null,
    share       int                                   not null,
    start_time  varchar(32)                           not null,
    end_time    varchar(32)                           null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null,
    updated_at  datetime    default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
)
    charset = utf8mb3;

create index bs_pos_index
    on future_fund_bsp_share (trading_day, bsp_id, start_time);

create table future_trade_task
(
    id             int auto_increment
        primary key,
    config_id      int                                    null,
    fund_code      varchar(255)                           not null,
    fund_id        int                                    not null,
    said           varchar(255)                           not null,
    task_type      varchar(255)                           not null,
    scheduled_time time                                   not null,
    task_tag       varchar(255)                           not null,
    target         varchar(512)                           null,
    trade_info     varchar(255)                           not null,
    trading_day    date                                   not null,
    status         int          default 1                 not null comment '1 启用；2 废弃',
    updated_at     datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    created_at     datetime     default CURRENT_TIMESTAMP null,
    updater        varchar(255) default ''                null comment '更新者，可作为修改批次号'
)
    collate = utf8mb4_unicode_ci;

create index idx_trade_task_trading_day
    on future_trade_task (trading_day);

create table future_trade_task_order_result
(
    id             int auto_increment
        primary key,
    trading_day    date                               not null,
    task_id        int                                not null,
    cli_basket_id  varchar(128)                       null,
    basket_id      varchar(64)                        null,
    symbol         varchar(64)                        null,
    side           varchar(64)                        null,
    offset         varchar(64)                        null,
    hedge          varchar(64)                        null,
    quantity       int                                null,
    rhino_quantity int                                null,
    error_code     varchar(255)                       null,
    error_text     varchar(512)                       null,
    created_at     datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
)
    collate = utf8mb4_unicode_ci;

create index idx0
    on future_trade_task_order_result (trading_day, task_id);

create table future_trade_task_status
(
    id          int auto_increment
        primary key,
    trading_day date                               not null,
    task_id     int                                not null,
    task_status int                                not null,
    remark      varchar(512)                       null,
    created_at  datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
)
    collate = utf8mb4_unicode_ci;

create table index_bar
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    minute      time                                  not null,
    symbol      varchar(255)                          not null,
    pre_close   decimal(18, 6)                        not null,
    close       decimal(18, 6)                        not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index index_bar
    on index_bar (trading_day, minute);

create table index_bar_status
(
    id          int auto_increment
        primary key,
    trading_day varchar(10)                           not null,
    minute      time                                  not null,
    updater     varchar(25) default 'bs'              not null,
    created_at  timestamp   default CURRENT_TIMESTAMP not null
)
    charset = utf8mb3;

create index index_bar_status
    on index_bar_status (trading_day);

create table is_info
(
    is_id        int auto_increment
        primary key,
    is_name      varchar(255)                           not null,
    is_name_en   varchar(255)                           not null,
    is_detail    varchar(255)                           not null,
    is_full_name varchar(255)                           not null,
    is_type      varchar(255)                           not null,
    status       tinyint      default 1                 not null comment '是否启用：0-否，1-是, -1 未知',
    updater      varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at   datetime     default CURRENT_TIMESTAMP null,
    updated_at   datetime     default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    has_bsp      tinyint      default 0                 null comment '是否关联bsp，0：否，1：是； 择时、现金等没有关联的bsp',
    sa_type      varchar(255)                           null comment '策略账号类型，用于择时类产品，生成黑名单任务用途',
    constraint uni_idx_is_full_name
        unique (is_full_name)
);

create table cfg_fund_is_copy1
(
    id         bigint auto_increment
        primary key,
    fund_id    int                                    not null,
    is_id      int                                    not null,
    wt         double                                 not null,
    start_date date                                   not null,
    end_date   date                                   null,
    start_time time                                   null,
    end_time   time                                   null,
    updater    varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at datetime     default CURRENT_TIMESTAMP null,
    updated_at datetime     default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    src_is_id  int                                    null comment '针对变更is_bsp的场景，记录变更来源',
    constraint cfg_fund_is_copy1_ibfk_1
        foreign key (is_id) references is_info (is_id)
);

create index idx_fund_is
    on cfg_fund_is_copy1 (fund_id, is_id);

create index is_id
    on cfg_fund_is_copy1 (is_id);

create table cfg_fund_is_unuse
(
    id         bigint auto_increment
        primary key,
    fund_id    int                                    not null,
    is_id      int                                    not null,
    wt         double                                 not null,
    start_date date                                   not null,
    end_date   date                                   null,
    start_time time                                   null,
    end_time   time                                   null,
    updater    varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at datetime     default CURRENT_TIMESTAMP null,
    updated_at datetime     default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    constraint cfg_fund_is_unuse_ibfk_1
        foreign key (is_id) references is_info (is_id)
)
    charset = utf8mb4;

create index idx_fund_is
    on cfg_fund_is_unuse (fund_id, is_id);

create index is_id
    on cfg_fund_is_unuse (is_id);

create table sa_transaction
(
    id                bigint auto_increment
        primary key,
    fund_id           bigint                                not null comment '基金id',
    fund_asset_origin decimal(18, 6)                        not null comment '基金产品初始资产',
    fund_asset        decimal(18, 6)                        not null comment '基金产品资产',
    bsp_type          varchar(50)                           null comment 'stock|future',
    sa_type           varchar(50)                           null comment '策略账户类型',
    wt                double                                null comment '策略账号占fund所有策略账号比重',
    sa_asset_origin   decimal(18, 6)                        not null comment '策略账号初始资产',
    sa_asset          decimal(18, 6)                        not null comment '策略账号变更后资产',
    net_inflow        decimal(18, 6)                        not null comment '资产变化值',
    updater           varchar(50) default ''                null comment '更新者，可作为修改批次号',
    trading_day       date                                  not null comment '交易日',
    created_at        datetime    default CURRENT_TIMESTAMP null,
    updated_at        datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create index idx_fund_id
    on sa_transaction (fund_id);

create index idx_trading_day
    on sa_transaction (trading_day);

create table sync_bsp_sp2sss_status
(
    id                  bigint auto_increment
        primary key,
    sss_bsp_id          bigint                                 null comment '实盘bsp id',
    sp_bspbase_id       bigint                                 null comment '策略池bsp id',
    new_sp_bsp_id       bigint                                 null comment '新增策略池bsp id',
    old_sp_bsp_id       bigint                                 null comment '旧的策略池bsp id',
    new_operation_batch varchar(255) default ''                null comment '本次同步批次',
    old_operation_batch varchar(255) default ''                null comment '关联的旧的同步批次',
    error_message       text                                   null comment '关联的旧的同步批次',
    status              tinyint      default 1                 not null comment '同步成功状态：1-成功,0-失败',
    created_at          datetime     default CURRENT_TIMESTAMP null,
    updated_at          datetime     default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create table trade_bs_portfolio
(
    id            int auto_increment
        primary key,
    bsp_name      varchar(255) default ''                not null comment 'bsp name, 全局唯一',
    name          varchar(255)                           not null,
    remark        varchar(255)                           null,
    level         int                                    not null,
    src_id        int                                    not null,
    sp_bspbase_id int          default -1                not null comment '策略池bspbase id',
    fund_id       int          default -1                not null comment '关联的fund_id，如果关联bsp1, 则为-1',
    sa_type       varchar(255) default ''                not null comment '策略账号类型，来自策略池bsp_info.sa_type',
    src_version   varchar(255)                           null,
    bsp_type      varchar(255) default 'stock'           not null comment 'stock|future',
    benchmark     varchar(255) default ''                null comment '用于配置is_bsp，筛选过滤用途',
    status        tinyint      default 1                 not null comment '是否启用：0-否，1-是, -1 未知',
    updater       varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at    datetime     default CURRENT_TIMESTAMP not null,
    updated_at    datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create table trade_bs_portfolio_detail
(
    id              int auto_increment
        primary key,
    bs_portfolio_id int                                    not null,
    bs_id           int                                    not null,
    sp_bsp_id       int          default -1                not null comment '策略池bsp id, 只填充bsp1 与 bs 关系中的bsp1',
    wt              double                                 not null,
    start_date      date                                   not null,
    end_date        date                                   null,
    start_time      time                                   null,
    end_time        time                                   null,
    updater         varchar(255) default ''                null comment '更新者，可作为修改批次号',
    created_at      datetime     default CURRENT_TIMESTAMP null,
    updated_at      datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create table trade_bs_portfolio_detail_snp
(
    id              int auto_increment
        primary key,
    bs_portfolio_id int                                    not null,
    bs_id           int                                    not null,
    wt              double                                 not null,
    trading_day     date                                   not null,
    updated_at      datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    created_at      datetime     default CURRENT_TIMESTAMP null,
    updater         varchar(255) default ''                null comment '更新者，可作为修改批次号'
);

create table trade_target_snp
(
    id          bigint auto_increment
        primary key,
    trading_day date                                  not null comment '交易日',
    for_fund    bigint                                not null comment '基金id',
    target_id   bigint                                not null comment 'target_id',
    target_name varchar(255)                          not null comment '投资策略名称',
    fund_id     bigint                                not null comment '基金id',
    sa_type     varchar(50)                           null comment '策略账户类型',
    bsp_type    varchar(255)                          null comment 'stock|future',
    group_id    int                                   not null comment '分组group_id',
    bsp_id      bigint                                null comment '分组group_id',
    wt          double                                null comment 'weight',
    updater     varchar(50) default ''                null comment '更新者，可作为修改批次号',
    created_at  datetime    default CURRENT_TIMESTAMP null,
    updated_at  datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create index idx_trading_day
    on trade_target_snp (trading_day);

create index idx_updater
    on trade_target_snp (updater);

create table trade_task
(
    id             int auto_increment
        primary key,
    config_id      int                                    null,
    fund_code      varchar(255)                           not null,
    fund_id        int                                    not null,
    said           varchar(255)                           not null,
    task_type      varchar(255)                           not null,
    scheduled_time time                                   not null,
    task_tag       varchar(255)                           not null,
    target         varchar(512)                           null,
    net_inflow     double                                 null,
    sell_ratio     double                                 null,
    trade_info     varchar(255)                           not null,
    trading_day    date                                   not null,
    status         int          default 1                 not null comment '1 启用；2 废弃',
    updated_at     datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    created_at     datetime     default CURRENT_TIMESTAMP null,
    updater        varchar(255) default ''                null comment '更新者，可作为修改批次号'
)
    collate = utf8mb4_unicode_ci;

create index idx_trade_task_trading_day
    on trade_task (trading_day);

create table trade_task_config
(
    id             int auto_increment
        primary key,
    fund_code      varchar(255)                           not null,
    fund_id        int                                    not null,
    said           varchar(255)                           not null,
    task_type      varchar(255)                           not null,
    scheduled_time time                                   null,
    task_tag       varchar(255)                           not null,
    target         varchar(512)                           null,
    net_inflow     double                                 null,
    sell_ratio     double                                 null,
    trade_info     varchar(255)                           not null,
    start_date     date                                   not null,
    end_date       date                                   null,
    updated_at     datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    created_at     datetime     default CURRENT_TIMESTAMP null,
    updater        varchar(255) default ''                null comment '更新者，可作为修改批次号'
);

create table trade_task_status
(
    id          int auto_increment
        primary key,
    trading_day date                               not null,
    task_id     int                                not null,
    task_status int                                not null,
    remark      varchar(255)                       null,
    net_amount  double                             not null,
    buy_amount  double                             not null,
    sell_amount double                             not null,
    created_at  datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
)
    collate = utf8mb4_unicode_ci;

create table trade_time
(
    time     varchar(8) null,
    time_a30 varchar(8) null
);

create index trade_time_index
    on trade_time (time, time_a30);

create table trading_day_list
(
    trading_day     varchar(255) null,
    ID              int          null,
    pre_trading_day varchar(255) null,
    pre_id          int          null
)
    collate = utf8mb4_unicode_ci;

create table write_trade_target_status
(
    id            bigint auto_increment
        primary key,
    trading_day   date                                  not null comment '交易日',
    error_message text                                  null comment '错误信息',
    status        tinyint     default 1                 not null comment '同步成功状态：1-成功,0-失败',
    task_type     varchar(50) default ''                null comment 'cover_all|bs_sync|basis_trade',
    metrics       text                                  null comment '变更指标',
    updater       varchar(50) default ''                null comment '更新者，可作为修改批次号',
    created_at    datetime    default CURRENT_TIMESTAMP null,
    updated_at    datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

