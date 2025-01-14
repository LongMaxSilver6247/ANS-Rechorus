import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from models.BaseModel import GeneralModel

class ANS(GeneralModel):
	reader = 'BaseReader'
	runner = 'BaseRunner'
	extra_log_args = ['embedding_size']

	@staticmethod
	def parse_model_args(parser):
		parser.add_argument('--embedding_size', type=int, default=64,
							help='Size of embedding vectors.')
		return GeneralModel.parse_model_args(parser)

	def __init__(self, args, corpus):
		super().__init__(args, corpus)
		self.embedding_size = args.embedding_size
		self.num_neg = args.num_neg
		self.batch_size = args.batch_size
		self.l2 = args.l2
		self.user_num = corpus.n_users
		self.item_num = corpus.n_items

		self._define_params()
		self.apply(self.init_weights)


	def _define_params(self):
		# 定义嵌入层
		self.user_embedding = nn.Embedding(self.user_num, self.embedding_size)
		self.item_embedding = nn.Embedding(self.item_num, self.embedding_size)

	def forward(self, feed_dict):
		user_ids = feed_dict['user_id']  # [batch_size]
		item_ids = feed_dict['item_id']  # [batch_size, -1]

		user_emb = self.user_embedding(user_ids)
		item_emb = self.item_embedding(item_ids)

		prediction = (user_emb[:, None, :] * item_emb).sum(dim=-1)  # [batch_size, -1]
		user_emb = user_emb.repeat(1,item_ids.shape[1]).view(item_ids.shape[0],item_ids.shape[1],-1)
		item_emb = item_emb
		l2_loss = self.l2 * (torch.sum(user_emb ** 2) + torch.sum(item_emb ** 2))
		out_dict = {'prediction': prediction.view(feed_dict['batch_size'], -1), 
			  		'u_v': user_emb, 
			  		'i_v':item_emb, 
			  		'l2_loss': l2_loss}
		return out_dict


	def loss(self, out_dict):
		prediction = out_dict['prediction']
		pos_pred, neg_pred = prediction[:, 0], prediction[:, 1:]
		loss = -torch.mean(torch.log(torch.sigmoid(pos_pred[:, None] - neg_pred)))
		loss += out_dict['l2_loss']
		return loss


	class Dataset(GeneralModel.Dataset):
		def __init__(self, model, corpus, phase):
			super().__init__(model, corpus, phase)
			if self.phase == 'train':
				interaction_df = pd.DataFrame({
					'user_id': self.data['user_id'],
					'item_id': self.data['item_id']
				})
				all_item_ids = pd.Series(range(self.corpus.n_items), name='item_id')
				interaction_df = pd.concat([interaction_df, all_item_ids.to_frame()], ignore_index=True)
				self.interaction_df = interaction_df.drop_duplicates(subset=['item_id'])

		def _get_feed_dict(self, index):
			user_id, target_item = self.data['user_id'][index], self.data['item_id'][index]
			if self.phase != 'train' and self.model.test_all:
				neg_items = np.arange(1, self.corpus.n_items)
			else:
				neg_items = self.data['neg_items'][index]
			item_ids = np.concatenate([[target_item], neg_items]).astype(int)
			feed_dict = {
				'user_id': user_id,
				'item_id': item_ids
			}
			return feed_dict

		def actions_before_epoch(self):
			neg_items = np.random.randint(1, self.corpus.n_items, size=(len(self), self.model.num_neg))
			for i, u in enumerate(self.data['user_id']):
				clicked_set = self.corpus.train_clicked_set[u]
				for j in range(self.model.num_neg):
					while neg_items[i][j] in clicked_set:
						# Augment negative sampling
						neg_items[i][j] = self._augmented_negative_sample(u, clicked_set)
			self.data['neg_items'] = neg_items

		def _augmented_negative_sample(self, user_id, clicked_set):
			item_similarities = self._compute_item_popularity()
			available_items = list(set(range(self.corpus.n_items)) - clicked_set)
			weighted_items = [(item, item_similarities[item]) for item in available_items]
			weighted_items.sort(key=lambda x: x[1], reverse=True)  # 按照相似度降序排列
			sampled_item = weighted_items[np.random.choice(len(weighted_items))][0]
			return sampled_item

		def _compute_item_popularity(self):
			item_interaction_count = self.interaction_df['item_id'].value_counts().reindex(range(self.corpus.n_items), fill_value=0).values

			# 归一化
			if item_interaction_count.max() - item_interaction_count.min() == 0:
				popularity_norm = np.zeros_like(item_interaction_count)
			else:
				popularity_norm = (item_interaction_count - item_interaction_count.min()) / (item_interaction_count.max() - item_interaction_count.min())
			
			return popularity_norm
