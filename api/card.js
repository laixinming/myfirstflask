import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

export default async function handler(req, res) {
  try {
    // 读取当前 cards 数据
    const cardsData = await redis.get('cards');
    let cards = cardsData ? JSON.parse(cardsData) : [];

    // POST：新增或更新卡片
    if (req.method === 'POST') {
      const { card } = req.body;
      if (!card || typeof card.id !== 'number') {
        return res.status(400).json({ error: 'Invalid card data' });
      }

      const index = cards.findIndex(c => c.id === card.id);
      if (index >= 0) {
        cards[index] = card;   // 更新
      } else {
        cards.push(card);      // 新增
      }

      // 保存回 Redis（字符串化）
      await redis.set('cards', JSON.stringify(cards));
      return res.status(200).json({ success: true });
    }

    // DELETE：删除卡片
    if (req.method === 'DELETE') {
      const { cardId } = req.body;
      if (typeof cardId !== 'number') {
        return res.status(400).json({ error: 'Invalid cardId' });
      }

      const filtered = cards.filter(c => c.id !== cardId);
      await redis.set('cards', JSON.stringify(filtered));
      return res.status(200).json({ success: true });
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.error('Redis operation error:', error);
    return res.status(500).json({ error: 'Internal server error', details: error.message });
  }
}
