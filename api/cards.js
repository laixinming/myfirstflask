import Redis from 'ioredis';

// 创建 Redis 客户端（连接字符串从环境变量读取）
const redis = new Redis(process.env.REDIS_URL);

export default async function handler(req, res) {
  // 只允许 GET
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // 从 Redis 获取 cards 字符串，默认返回空数组
    const cardsData = await redis.get('cards');
    const cards = cardsData ? JSON.parse(cardsData) : [];

    return res.status(200).json({ cards });
  } catch (error) {
    console.error('Redis GET error:', error);
    return res.status(500).json({ error: 'Internal server error', details: error.message });
  }
}
