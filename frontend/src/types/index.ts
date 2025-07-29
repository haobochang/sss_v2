// API响应类型定义
export interface Product {
  id: string;
  name: string;
  node_type: string;
  status: number;
  total_market_value: number;
  total_pnl: number;
  daily_return: number;
  strategy_count: number;
  last_updated?: string;
}

export interface ProductDetail extends Product {
  config_details?: any;
  tree_structure?: TreeNode;
  stats?: ProductStats;
  created_at?: string;
  updated_at?: string;
}

export interface ProductStats {
  total_market_value: number;
  total_pnl: number;
  daily_return: number;
  strategy_count: number;
}

export interface TreeNode {
  id: string;
  name: string;
  node_type: string;
  status: number;
  config_details?: any;
  total_market_value: number;
  total_pnl: number;
  positions: Position[];
  special_info?: any;
  children: TreeNode[];
  weight?: number;
}

export interface Position {
  id: string;
  node_id: string;
  trading_day?: string;
  symbol: string;
  position_type: string;
  quantity: number;
  cost_price?: number;
  market_value?: number;
  weight_in_node?: number;
}

export interface PortfolioNode {
  id: string;
  name: string;
  node_type: string;
  status: number;
  config_details?: any;
  source_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface Trade {
  id: string;
  product_node_id: string;
  trading_day?: string;
  basket_id: string;
  symbol: string;
  target_quantity: number;
  filled_quantity: number;
  status: string;
  created_at?: string;
}

export interface TradeAllocation {
  id: string;
  order_id: string;
  leaf_node_id: string;
  allocated_quantity: number;
}

// 中性策略敞口信息
export interface ExposureInfo {
  long_exposure: number;
  short_exposure: number;
  net_exposure: number;
}

// API响应包装类型
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
} 