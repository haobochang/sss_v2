import React, { useState, useEffect } from 'react';
import { Table, Card, Row, Col, Statistic, Spin, message } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined, DollarOutlined, LineChartOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { Product } from '../types';
import { productApi } from '../services/api';
import ReactECharts from 'echarts-for-react';

const ProductList: React.FC = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchProducts();
    }, []);

    const fetchProducts = async () => {
        try {
            setLoading(true);
            const data = await productApi.getProducts();
            setProducts(data);
        } catch (error) {
            message.error('获取产品列表失败');
            console.error('Error fetching products:', error);
        } finally {
            setLoading(false);
        }
    };

    const columns = [
        {
            title: '产品名称',
            dataIndex: 'name',
            key: 'name',
            render: (text: string, record: Product) => (
                <a onClick={() => navigate(`/product/${record.id}`)}>{text}</a>
            ),
        },
        {
            title: '总市值',
            dataIndex: 'total_market_value',
            key: 'total_market_value',
            render: (value: number) => `¥${(value / 10000).toFixed(2)}万`,
            sorter: (a: Product, b: Product) => a.total_market_value - b.total_market_value,
        },
        {
            title: '总盈亏',
            dataIndex: 'total_pnl',
            key: 'total_pnl',
            render: (value: number) => (
                <span style={{ color: value >= 0 ? '#52c41a' : '#ff4d4f' }}>
                    {value >= 0 ? '+' : ''}¥{(value / 10000).toFixed(2)}万
                </span>
            ),
            sorter: (a: Product, b: Product) => a.total_pnl - b.total_pnl,
        },
        {
            title: '日收益率',
            dataIndex: 'daily_return',
            key: 'daily_return',
            render: (value: number) => (
                <span style={{ color: value >= 0 ? '#52c41a' : '#ff4d4f' }}>
                    {value >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
                    {(value * 100).toFixed(2)}%
                </span>
            ),
            sorter: (a: Product, b: Product) => a.daily_return - b.daily_return,
        },
        {
            title: '策略数量',
            dataIndex: 'strategy_count',
            key: 'strategy_count',
            render: (value: number) => `${value}个`,
        },
        {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            render: (status: number) => (
                <span style={{ color: status === 1 ? '#52c41a' : '#ff4d4f' }}>
                    {status === 1 ? '运行中' : '已停止'}
                </span>
            ),
        },
    ];

    const getChartOption = () => {
        const names = products.map(p => p.name);
        const marketValues = products.map(p => p.total_market_value / 10000);
        const pnls = products.map(p => p.total_pnl / 10000);

        return {
            title: {
                text: '产品市值与盈亏对比',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: ['总市值(万)', '总盈亏(万)'],
                top: 30
            },
            xAxis: {
                type: 'category',
                data: names,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '总市值(万)',
                    type: 'bar',
                    data: marketValues,
                    itemStyle: {
                        color: '#1890ff'
                    }
                },
                {
                    name: '总盈亏(万)',
                    type: 'bar',
                    data: pnls,
                    itemStyle: {
                        color: '#52c41a'
                    }
                }
            ]
        };
    };

    const getReturnChartOption = () => {
        const names = products.map(p => p.name);
        const returns = products.map(p => p.daily_return * 100);

        return {
            title: {
                text: '产品日收益率',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                formatter: '{b}: {c}%'
            },
            xAxis: {
                type: 'category',
                data: names,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value}%'
                }
            },
            series: [
                {
                    type: 'line',
                    data: returns,
                    itemStyle: {
                        color: '#1890ff'
                    },
                    areaStyle: {
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [
                                { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
                                { offset: 1, color: 'rgba(24, 144, 255, 0.1)' }
                            ]
                        }
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

    return (
        <div style={{ padding: '24px' }}>
            <h1 style={{ marginBottom: '24px' }}>量化产品管理</h1>

            {/* 统计卡片 */}
            <Row gutter={16} style={{ marginBottom: '24px' }}>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="产品总数"
                            value={products.length}
                            prefix={<LineChartOutlined />}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="总市值"
                            value={products.reduce((sum, p) => sum + p.total_market_value, 0) / 10000}
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
                            value={products.reduce((sum, p) => sum + p.total_pnl, 0) / 10000}
                            precision={2}
                            prefix={<DollarOutlined />}
                            suffix="万"
                            valueStyle={{ color: products.reduce((sum, p) => sum + p.total_pnl, 0) >= 0 ? '#3f8600' : '#cf1322' }}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="平均日收益率"
                            value={products.reduce((sum, p) => sum + p.daily_return, 0) / products.length * 100}
                            precision={2}
                            suffix="%"
                            valueStyle={{ color: products.reduce((sum, p) => sum + p.daily_return, 0) >= 0 ? '#3f8600' : '#cf1322' }}
                        />
                    </Card>
                </Col>
            </Row>

            {/* 图表 */}
            <Row gutter={16} style={{ marginBottom: '24px' }}>
                <Col span={12}>
                    <Card title="产品市值与盈亏对比">
                        <ReactECharts option={getChartOption()} style={{ height: '300px' }} />
                    </Card>
                </Col>
                <Col span={12}>
                    <Card title="产品日收益率">
                        <ReactECharts option={getReturnChartOption()} style={{ height: '300px' }} />
                    </Card>
                </Col>
            </Row>

            {/* 产品列表表格 */}
            <Card title="产品列表">
                <Table
                    columns={columns}
                    dataSource={products}
                    rowKey="id"
                    pagination={{
                        pageSize: 10,
                        showSizeChanger: true,
                        showQuickJumper: true,
                        showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条/共 ${total} 条`,
                    }}
                />
            </Card>
        </div>
    );
};

export default ProductList; 