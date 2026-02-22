import { kv } from '@vercel/kv';

export default async function handler(req, res) {
  try {
    // 读取当前所有卡片
    let cards = await kv.get('cards') || [];

    // POST 请求：添加新卡片或更新现有卡片
    if (req.method === 'POST') {
      const { card } = req.body;
      if (!card || typeof card.id !== 'number') {
        return res.status(400).json({ error: 'Invalid card data' });
      }

      // 查找是否已存在同 id 的卡片
      const index = cards.findIndex(c => c.id === card.id);
      if (index >= 0) {
        // 更新
        cards[index] = card;
      } else {
        // 新增
        cards.push(card);
      }

      // 保存回 KV
      await kv.set('cards', cards);
      return res.status(200).json({ success: true });
    }

    // DELETE 请求：删除指定 id 的卡片
    if (req.method === 'DELETE') {
      const { cardId } = req.body;
      if (typeof cardId !== 'number') {
        return res.status(400).json({ error: 'Invalid cardId' });
      }

      const filtered = cards.filter(c => c.id !== cardId);
      await kv.set('cards', filtered);
      return res.status(200).json({ success: true });
    }

    // 其他方法不允许
    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.error('KV operation error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
