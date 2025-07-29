import axios from 'axios';
import { Product, ProductDetail, TreeNode, Position, Trade } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// 产品相关API
export const productApi = {
  // 获取产品列表
  getProducts: async (): Promise<Product[]> => {
    const response = await api.get('/products');
    return response.data;
  },

  // 获取产品详情
  getProductDetail: async (productId: string): Promise<ProductDetail> => {
    const response = await api.get(`/products/${productId}`);
    return response.data;
  },

  // 获取产品树结构
  getProductTree: async (productId: string): Promise<TreeNode> => {
    const response = await api.get(`/products/${productId}/tree`);
    return response.data;
  },
};

// 持仓相关API
export const positionApi = {
  // 获取持仓列表
  getPositions: async (nodeId?: string, positionType?: string): Promise<Position[]> => {
    const params: any = {};
    if (nodeId) params.node_id = nodeId;
    if (positionType) params.position_type = positionType;
    
    const response = await api.get('/positions', { params });
    return response.data;
  },

  // 获取节点持仓
  getNodePositions: async (nodeId: string): Promise<Position[]> => {
    const response = await api.get(`/positions/node/${nodeId}`);
    return response.data;
  },
};

// 交易相关API
export const tradeApi = {
  // 获取交易列表
  getTrades: async (productNodeId?: string): Promise<Trade[]> => {
    const params: any = {};
    if (productNodeId) params.product_node_id = productNodeId;
    
    const response = await api.get('/trades', { params });
    return response.data;
  },
};

export default api; 