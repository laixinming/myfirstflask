import { kv } from '@vercel/kv';

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const cards = await kv.get('cards') || [];
    return res.status(200).json({ cards });
  } catch (error) {
    console.error('KV get error:', error);
    return res.status(500).json({ error: 'Internal server error', details: error.message });
  }
}
