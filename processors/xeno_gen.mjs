import { pipeline, env } from '@xenova/transformers';
import fs from 'fs';

const PATH = '';

const embedder = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
//console.log('Cache directory:', env.cacheDir);

//const jsonTxt = fs.readFileSync(PATH + 'Lovecraft_chunks.json', 'utf8');
const jsonTxt = fs.readFileSync(PATH + 'Aesop_chunks.json', 'utf8');

const chunkDict = JSON.parse(jsonTxt);

const embeddings = [];
for( let chunk of chunkDict ) {
  console.log('→',chunk.text);
  const result = await embedder(chunk.text, { pooling: 'mean', normalize: true });
  embeddings.push({
    title: chunk.title,
    story: chunk.story_id,
    authors: chunk.authors, 
    num: chunk.chunk_id,
    count: chunk.len,
    text: chunk.text,
    vector: Array.from(result.data)
  });
}

//fs.writeFileSync(PATH + 'Lovecraft_embeddings.json', JSON.stringify(embeddings));
fs.writeFileSync(PATH + 'Aesop_embeddings.json', JSON.stringify(embeddings));
