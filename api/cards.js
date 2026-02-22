import { kv } from '@vercel/kv';

export default async function handler(req, res) {
  // 只允许 GET 请求
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // 从 KV 中读取 cards，如果不存在则返回空数组
    const cards = await kv.get('cards') || [];
    return res.status(200).json({ cards });
  } catch (error) {
    console.error('KV get error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
