import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
    Card, Row, Col, Statistic, Spin, message, Tree, Descriptions,
    Table, Tag, Progress, Divider, Typography
} from 'antd';
import {
    DollarOutlined, LineChartOutlined, ArrowUpOutlined,
    ArrowDownOutlined, EyeOutlined
} from '@ant-design/icons';
import type { ProductDetail, TreeNode, Position } from '../types';
import { productApi } from '../services/api';
import ReactECharts from 'echarts-for-react';

const { Title, Text } = Typography;

const ProductDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [product, setProduct] = useState<ProductDetail | null>(null);
    const [loading, setLoading] = useState(true);
    const [selectedNode, setSelectedNode] = useState<TreeNode | null>(null);

    useEffect(() => {
        if (id) {
            fetchProductDetail();
        }
    }, [id]);

    const fetchProductDetail = async () => {
        try {
            setLoading(true);
            const data = await productApi.getProductDetail(id!);
            setProduct(data);
        } catch (error) {
            message.error('获取产品详情失败');
            console.error('Error fetching product detail:', error);
        } finally {
            setLoading(false);
        }
    };

    const renderTreeNode = (node: TreeNode): any => {
        const title = (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span>{node.name}</span>
                <div style={{ display: 'flex', gap: '8px' }}>
                    <Tag color={node.status === 1 ? 'green' : 'red'}>
                        {node.status === 1 ? '运行中' : '已停止'}
                    </Tag>
                    {node.weight && (
                        <Tag color="blue">{(node.weight * 100).toFixed(1)}%</Tag>
                    )}
                </div>
            </div>
        );

        return {
            title,
            key: node.id,
            children: node.children.map(child => renderTreeNode(child)),
            node: node,
        };
    };

    const getPositionColumns = () => [
        {
            title: '证券代码',
            dataIndex: 'symbol',
            key: 'symbol',
        },
        {
            title: '持仓类型',
            dataIndex: 'position_type',
            key: 'position_type',
            render: (type: string) => (
                <Tag color={type === 'TARGET' ? 'blue' : 'green'}>
                    {type === 'TARGET' ? '目标持仓' : '实际持仓'}
                </Tag>
            ),
        },
        {
            title: '数量',
            dataIndex: 'quantity',
            key: 'quantity',
            render: (value: number) => value.toLocaleString(),
        },
        {
            title: '成本价',
            dataIndex: 'cost_price',
            key: 'cost_price',
            render: (value: number) => value ? `¥${value.toFixed(2)}` : '-',
        },
        {
            title: '市值',
            dataIndex: 'market_value',
            key: 'market_value',
            render: (value: number) => value ? `¥${(value / 10000).toFixed(2)}万` : '-',
        },
        {
            title: '权重',
            dataIndex: 'weight_in_node',
            key: 'weight_in_node',
            render: (value: number) => value ? `${(value * 100).toFixed(2)}%` : '-',
        },
    ];

    const getExposureChartOption = (exposureInfo: any) => {
        return {
            title: {
                text: '中性策略敞口分析',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [
                {
                    type: 'pie',
                    radius: '50%',
                    data: [
                        { value: exposureInfo.long_exposure, name: '多头敞口' },
                        { value: exposureInfo.short_exposure, name: '空头敞口' },
                        { value: Math.abs(exposureInfo.net_exposure), name: '净敞口' }
                    ],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
    };

    const getPositionChartOption = (positions: Position[]) => {
        const symbols = positions.map(p => p.symbol);
        const quantities = positions.map(p => p.quantity);
        const marketValues = positions.map(p => p.market_value || 0);

        return {
            title: {
                text: '持仓分布',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: ['持仓数量', '市值(万)'],
                top: 30
            },
            xAxis: {
                type: 'category',
                data: symbols
            },
            yAxis: [
                {
                    type: 'value',
                    name: '数量'
                },
                {
                    type: 'value',
                    name: '市值(万)',
                    axisLabel: {
                        formatter: '{value}万'
                    }
                }
            ],
            series: [
                {
                    name: '持仓数量',
                    type: 'bar',
                    data: quantities,
                    itemStyle: {
                        color: '#1890ff'
                    }
                },
                {
                    name: '市值(万)',
                    type: 'line',
                    yAxisIndex: 1,
                    data: marketValues.map(v => v / 10000),
                    itemStyle: {
                        color: '#52c41a'
                    }
                }
            ]
        };
    };

    if (loading) {
        return (
            <div style={{ textAlign: 'center', padding: '50px' }}>
                <Spin size="large" />
            </div>
        );
    }

    if (!product) {
        return <div>产品不存在</div>;
    }

    const treeData = product.tree_structure ? [renderTreeNode(product.tree_structure)] : [];

    return (
        <div style={{ padding: '24px' }}>
            <Title level={2}>{product.name}</Title>

            {/* 产品统计信息 */}
            <Row gutter={16} style={{ marginBottom: '24px' }}>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="总市值"
                            value={product.total_market_value / 10000}
                            precision={2}
                            prefix={<DollarOutlined />}
                            suffix="万"
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="总盈亏"
                            value={product.total_pnl / 10000}
                            precision={2}
                            prefix={<DollarOutlined />}
                            suffix="万"
                            valueStyle={{ color: product.total_pnl >= 0 ? '#3f8600' : '#cf1322' }}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="日收益率"
                            value={product.daily_return * 100}
                            precision={2}
                            suffix="%"
                            valueStyle={{ color: product.daily_return >= 0 ? '#3f8600' : '#cf1322' }}
                            prefix={product.daily_return >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="策略数量"
                            value={product.strategy_count}
                            prefix={<LineChartOutlined />}
                        />
                    </Card>
                </Col>
            </Row>

            <Row gutter={16}>
                {/* 左侧：树形结构 */}
                <Col span={12}>
                    <Card title="投资组合结构" extra={<EyeOutlined />}>
                        <Tree
                            treeData={treeData}
                            onSelect={(selectedKeys, info) => {
                                if (info.node.node) {
                                    setSelectedNode(info.node.node);
                                }
                            }}
                            defaultExpandAll
                        />
                    </Card>
                </Col>

                {/* 右侧：选中节点详情 */}
                <Col span={12}>
                    <Card title="节点详情">
                        {selectedNode ? (
                            <div>
                                <Descriptions column={1}>
                                    <Descriptions.Item label="节点名称">{selectedNode.name}</Descriptions.Item>
                                    <Descriptions.Item label="节点类型">{selectedNode.node_type}</Descriptions.Item>
                                    <Descriptions.Item label="状态">
                                        <Tag color={selectedNode.status === 1 ? 'green' : 'red'}>
                                            {selectedNode.status === 1 ? '运行中' : '已停止'}
                                        </Tag>
                                    </Descriptions.Item>
                                    <Descriptions.Item label="总市值">
                                        ¥{(selectedNode.total_market_value / 10000).toFixed(2)}万
                                    </Descriptions.Item>
                                    <Descriptions.Item label="总盈亏">
                                        <span style={{ color: selectedNode.total_pnl >= 0 ? '#52c41a' : '#ff4d4f' }}>
                                            {selectedNode.total_pnl >= 0 ? '+' : ''}¥{(selectedNode.total_pnl / 10000).toFixed(2)}万
                                        </span>
                                    </Descriptions.Item>
                                </Descriptions>

                                {/* 中性策略特殊信息 */}
                                {selectedNode.special_info?.exposure && (
                                    <div style={{ marginTop: '16px' }}>
                                        <Divider>中性策略敞口</Divider>
                                        <Row gutter={16}>
                                            <Col span={8}>
                                                <Progress
                                                    type="circle"
                                                    percent={selectedNode.special_info.exposure.long_exposure * 100}
                                                    format={percent => `${percent?.toFixed(1)}%`}
                                                    strokeColor="#52c41a"
                                                />
                                                <div style={{ textAlign: 'center', marginTop: '8px' }}>
                                                    <Text>多头敞口</Text>
                                                </div>
                                            </Col>
                                            <Col span={8}>
                                                <Progress
                                                    type="circle"
                                                    percent={selectedNode.special_info.exposure.short_exposure * 100}
                                                    format={percent => `${percent?.toFixed(1)}%`}
                                                    strokeColor="#ff4d4f"
                                                />
                                                <div style={{ textAlign: 'center', marginTop: '8px' }}>
                                                    <Text>空头敞口</Text>
                                                </div>
                                            </Col>
                                            <Col span={8}>
                                                <Progress
                                                    type="circle"
                                                    percent={Math.abs(selectedNode.special_info.exposure.net_exposure) * 100}
                                                    format={percent => `${percent?.toFixed(1)}%`}
                                                    strokeColor={selectedNode.special_info.exposure.net_exposure >= 0 ? '#52c41a' : '#ff4d4f'}
                                                />
                                                <div style={{ textAlign: 'center', marginTop: '8px' }}>
                                                    <Text>净敞口</Text>
                                                </div>
                                            </Col>
                                        </Row>
                                    </div>
                                )}

                                {/* 持仓信息 */}
                                {selectedNode.positions && selectedNode.positions.length > 0 && (
                                    <div style={{ marginTop: '16px' }}>
                                        <Divider>持仓信息</Divider>
                                        <Table
                                            columns={getPositionColumns()}
                                            dataSource={selectedNode.positions}
                                            rowKey="id"
                                            size="small"
                                            pagination={false}
                                        />
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div style={{ textAlign: 'center', color: '#999' }}>
                                请选择左侧节点查看详情
                            </div>
                        )}
                    </Card>
                </Col>
            </Row>

            {/* 图表区域 */}
            {selectedNode && (
                <Row gutter={16} style={{ marginTop: '24px' }}>
                    {selectedNode.special_info?.exposure && (
                        <Col span={12}>
                            <Card title="敞口分析">
                                <ReactECharts
                                    option={getExposureChartOption(selectedNode.special_info.exposure)}
                                    style={{ height: '300px' }}
                                />
                            </Card>
                        </Col>
                    )}
                    {selectedNode.positions && selectedNode.positions.length > 0 && (
                        <Col span={selectedNode.special_info?.exposure ? 12 : 24}>
                            <Card title="持仓分布">
                                <ReactECharts
                                    option={getPositionChartOption(selectedNode.positions)}
                                    style={{ height: '300px' }}
                                />
                            </Card>
                        </Col>
                    )}
                </Row>
            )}
        </div>
    );
};

export default ProductDetail; 