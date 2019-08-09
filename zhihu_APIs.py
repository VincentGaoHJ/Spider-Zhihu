# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time  : 2019/7/14 18:39
# author : strangestring
# github : https://github.com/strangestring
# mailbox: 1814232115@qq.com


import time


class ZhiHu:
    def __init__(self):
        """
        知乎API的核心,私有子类封装了一些API
        """
        self.members = self._Members()
        self.articles = self._Articles()
        self.answers = self._Answers()
        self.questions = self._Questions()
        self.pins = self._Pins()
        self.topic = self._Topic()
    
    
    class _Members:
        @staticmethod
        def info(url_token, query_args=None):
            """

            :param url_token:
            :param query_args:'allow_message','is_followed','is_following','description','is_org','is_blocking','employments','answer_count','follower_count','articles_count','gender','thanked_count','favorited_count','badge[?(type=best_answerer)].topics'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}?{additional_query_items}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}'
        
        
        @staticmethod
        def followees(url_token, offset=0, limit=20, query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args:
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/followees?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/followees?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def followers(url_token, offset=0, limit=20, query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args:
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/followers?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/followers?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def activities(url_token, after_id=int(time.time()), limit=7, session_id=1099803331731554304):
            """
            before_id版API等同于after_id=int(time.time)的情形
            desktop=True无影响
            :param url_token:
            :param after_id: offset的另一种形式
            :param session_id:
            :param limit:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/members/{url_token}/activities?limit={limit}&session_id={session_id}&after_id={after_id}&desktop=True'
        
        
        @staticmethod
        def pins(url_token, offset=0, limit=20, query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args:
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/pins?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/pins?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def answers(url_token, offset=0, limit=20, sort_by='voteups', query_args=None):
            """
            :param url_token:
            :param offset:
            :param limit:
            :param sort_by:'voteups'/'created'
            :param query_args:'is_normal','admin_closed_comment','reward_info',
            'is_collapsed','annotation_action','annotation_detail','collapse_reason',
            'collapsed_by','suggest_edit','comment_count','can_comment','content',
            'voteup_count','reshipment_settings','comment_permission','mark_infos',
            'created_time','updated_time','review_info','question','excerpt',
            'is_labeled','label_info','relationship.is_authorized','voting',
            'is_author','is_thanked','is_nothelp',
            'is_recognized;data[*].author.badge[?(type=best_answerer)].topics'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/answers?{additional_query_items}&offset={offset}&limit={limit}&sort_by={sort_by}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/answers?offset={offset}&limit={limit}&sort_by={sort_by}'
        
        
        @staticmethod
        def articles(url_token, offset=0, limit=20, sort_by='voteups', query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param sort_by:'voteups'/'created'
            :param query_args:'comment_count','suggest_edit','is_normal',
            'thumbnail_extra_info','thumbnail','can_comment','comment_permission',
            'admin_closed_comment','content','voteup_count','created','updated',
            'upvoted_followees','voting','review_info','is_labeled',
            'label_info;data[*].author.badge[?(type=best_answerer)].topics'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/articles?{additional_query_items}&offset={offset}&limit={limit}&sort_by={sort_by}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/articles?offset={offset}&limit={limit}&sort_by={sort_by}'
        
        
        @staticmethod
        def questions(url_token, offset=0, limit=20, query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args:'created','answer_count','follower_count','author',
            'admin_closed_comment'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/questions?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/questions?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def column_contributions(url_token, offset=0, limit=20, query_args=None):
            """
            :param url_token:
            :param offset:
            :param limit:
            :param query_args:'column.intro','followers','articles_count'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/column-contributions?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/column-contributions?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def favlists(url_token, offset=0, limit=20, query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args:'updated_time','answer_count','follower_count','is_public'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/favlists?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/favlists?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def following_columns(url_token, offset=0, limit=20, query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args:'intro','followers','articles_count'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/following-columns?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/following-columns?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def following_topic_contributions(url_token, offset=0, limit=20, query_args=None, ):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args: 'topic','introduction'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/following-topic-contributions?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/following-topic-contributions?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def following_questions(url_token, offset=0, limit=20, query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args: 'created','answer_count','follower_count','author'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/following-questions?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/following-questions?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def following_favlists(url_token, offset=0, limit=20, query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param query_args: 'updated_time','answer_count','follower_count'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/following-favlists?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/following-favlists?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def marked_answers(url_token, offset=0, limit=20, sort_by='voteups', query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param sort_by:
            :param query_args:'is_normal','admin_closed_comment','reward_info',
            'is_collapsed','annotation_action','annotation_detail','collapse_reason',
            'collapsed_by','suggest_edit','comment_count','can_comment','content',
            'voteup_count','reshipment_settings','comment_permission','mark_infos',
            'created_time','updated_time','review_info','question','excerpt',
            'is_labeled','label_info','relationship.is_authorized','voting',
            'is_author','is_thanked','is_nothelp',
            'is_recognized;data[*].author.badge[?(type=best_answerer)].topics'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/marked-answers?{additional_query_items}&offset={offset}&limit={limit}&sort_by={sort_by}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/marked-answers?offset={offset}&limit={limit}&sort_by={sort_by}'
        
        
        @staticmethod
        def included_articles(url_token, offset=0, limit=20, sort_by='voteups', query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param sort_by:
            :param query_args:
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/included-articles?{additional_query_items}&offset={offset}&limit={limit}&sort_by={sort_by}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/included-articles?offset={offset}&limit={limit}&sort_by={sort_by}'
        
        
        @staticmethod
        def mutuals(url_token, offset=0, limit=10, sort_by='voteups', query_args=None):
            """

            :param url_token:
            :param offset:
            :param limit:
            :param sort_by:
            :param query_args:'answer_count','articles_count','gender','follower_count',
            'is_followed','is_following','badge[?(type=best_answerer)].topics'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/members/{url_token}/relations/mutuals?{additional_query_items}&offset={offset}&limit={limit}&sort_by={sort_by}'
            else:
                return f'https://www.zhihu.com/api/v4/members/{url_token}/relations/mutuals?offset={offset}&limit={limit}&sort_by={sort_by}'
    
    
    class _Articles:
        @staticmethod
        def info(url_token):  # todo:加上query_args
            """

            :param url_token:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/articles/{url_token}'
        
        
        @staticmethod
        def likers(article_id, offset=0, limit=20, query_args=None):
            """

            :param article_id:
            :param offset:
            :param limit:
            :param query_args:
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/articles/{article_id}/likers?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/articles/{article_id}/likers?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def concerned_upvoters(article_id):
            """

            :param article_id:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/articles/{article_id}/concerned_upvoters'
        
        
        @staticmethod
        def root_comments(article_id, offset=0, limit=20, order='normal'):
            """

            :param article_id:
            :param offset:
            :param limit:
            :param order:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/articles/{article_id}/root_comments?limit={limit}&offset={offset}&order={order}&status=open'
        
        
        @staticmethod
        def comments(article_id, offset=0, limit=20, order='reverse'):
            """

            :param article_id:
            :param offset:
            :param limit:
            :param order:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/articles/{article_id}/root_comments?limit={limit}&offset={offset}&order={order}&status=open'
    
    
    class _Answers:
        @staticmethod
        def info(url_token):
            """

            :param url_token:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/answsers/{url_token}'
        
        
        @staticmethod
        def voters(answer_id, offset=0, limit=10, query_args=None):
            """

            :param answer_id:
            :param offset:
            :param limit:
            :param query_args: 'answer_count','articles_count','follower_count',
            'gender','is_followed','is_following','badge'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/answers/{answer_id}/voters?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/answers/{answer_id}/voters?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def concerned_upvoters(answer_id, offset=0, limit=20, query_args=None):
            """

            :param answer_id:
            :param offset:
            :param limit:
            :param query_args:
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/answers/{answer_id}/concerned_upvoters?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/answers/{answer_id}/concerned_upvoters?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def favlists(answer_id, offset=0, limit=20, query_args=None):
            """

            :param answer_id:
            :param offset:
            :param limit:
            :param query_args:
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/answers/{answer_id}/favlists?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/answers/{answer_id}/favlists?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def root_comments(answer_id, offset=0, limit=20, order='normal'):
            """

            :param answer_id:
            :param offset:
            :param limit:
            :param order:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/answers/{answer_id}/root_comments?limit={limit}&offset={offset}&order={order}&status=open'
        
        
        @staticmethod
        def comments(answer_id, offset=0, limit=20, order='reverse'):
            """

            :param answer_id:
            :param offset:
            :param limit:
            :param order:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/answers/{answer_id}/root_comments?limit={limit}&offset={offset}&order={order}&status=open'
    
    
    class _Questions:
        @staticmethod
        def info(url_token):
            """

            :param url_token:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/questions/{url_token}'
        
        
        @staticmethod
        def followers(question_id, offset=0, limit=20, query_args=None):
            """

            :param question_id:
            :param offset:
            :param limit:
            :param query_args:'gender','answer_count','articles_count',
            'follower_count','is_following','is_followed'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/questions/{question_id}/followers?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/questions/{question_id}/followers?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def concerned_followers(question_id, offset=0, limit=20, query_args=None):
            """

            :param question_id:
            :param offset:
            :param limit:
            :param query_args:
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/questions/{question_id}/concerned_followers?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/questions/{question_id}/concerned_followers?offset={offset}&limit={limit}'
        
        
        @staticmethod
        def answers(question_id, offset=0, limit=20, sort_by='default', query_args=None):
            """

            :param question_id:
            :param offset:
            :param limit:
            :param sort_by: 'default','updated'
            :param query_args: 'is_normal','admin_closed_comment','reward_info',
            'is_collapsed','annotation_action','annotation_detail',
            'collapse_reason','is_sticky','collapsed_by','suggest_edit',
            'comment_count','can_comment','content','editable_content',
            'voteup_count','reshipment_settings','comment_permission',
            'created_time','updated_time','review_info','relevant_info',
            'question','excerpt','relationship.is_authorized','is_author',
            'voting','is_thanked','is_nothelp','is_labeled','is_recognized',
            'paid_info','paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count','badge[*].topics'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/questions/{question_id}/answers?{additional_query_items}&offset={offset}&limit={limit}&sort_by={sort_by}'
            else:
                return f'https://www.zhihu.com/api/v4/questions/{question_id}/answers?offset={offset}&limit={limit}&sort_by={sort_by}'
        
        
        @staticmethod
        def root_comments(question_id, offset=0, limit=20, order='normal'):
            """

            :param question_id:
            :param offset:
            :param limit:
            :param order:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/articles/{question_id}/root_comments?limit={limit}&offset={offset}&order={order}&status=open'
        
        
        @staticmethod
        def comments(question_id, offset=0, limit=20, order='reverse'):
            """

            :param question_id:
            :param offset:
            :param limit:
            :param order:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/articles/{question_id}/root_comments?limit={limit}&offset={offset}&order={order}&status=open'
        
        
        @staticmethod
        def similar_questions(question_id, offset=0, limit=5, query_args=None):
            """

            :param question_id:
            :param offset:
            :param limit: 5
            :param query_args: 'answer_count','author','follower_count'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/questions/{question_id}/similar-questions?{additional_query_items}&offset={offset}&limit={limit}'
            else:
                return f'https://www.zhihu.com/api/v4/questions/{question_id}/similar-questions?offset={offset}&limit={limit}'
    
    
    class _Pins:
        @staticmethod
        def info(pin_id):
            """

            :param pin_id:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/pins/{pin_id}'
        
        
        @staticmethod
        def comments(pin_id, offset=0, limit=20, order='reverse'):
            """
            :param pin_id:
            :param offset:
            :param limit:
            :param order: 'normal','reverse'
            :return:
            """
            return f'https://www.zhihu.com/api/v4/pins/{pin_id}/comments?order={order}&limit={limit}&offset={offset}&status=open'
    
    
    class _Topic:
        @staticmethod
        def info(topic_id):
            """
            
            :param topic_id:
            :return:
            """
            return f'https://www.zhihu.com/api/v4/topics/{topic_id}'
        
        @staticmethod
        def followers(topic_id, offset=0, limit=20, query_args=None):
            """

            :param topic_id:
            :param offset:
            :param limit:
            :param query_args:'gender','answer_count','articles_count',
            'follower_count','is_following','is_followed'
            :return:
            """
            if query_args:
                additional_query_items = f'include=data[*].{",".join(query_args)}'
                return f'https://www.zhihu.com/api/v4/questions/{topic_id}/followers?{additional_query_items}&offset={offset}&limit={limit}'
            
            else:
                return f'https://www.zhihu.com/api/v4/questions/{topic_id}/followers?offset={offset}&limit={limit}'
        
        @staticmethod
        def timeline_question(topic_id, offset=0, limit=10, query_args=None):
            """
            
            :param topic_id:
            :param offset:
            :param limit:
            :param query_args:
            :return:
            """
            
            '''
            https://www.zhihu.com/api/v4/topics/20009759/feeds/timeline_question
?include=
.target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;

.target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;

.target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;

.target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;

data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;

data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;

data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;

data[?(target.type=question)].target.annotation_detail,comment_count;

&limit=10&offset=35
            '''
            return f'https://www.zhihu.com/api/v4/topics/{topic_id}/feeds/timeline_question?include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;&limit={limit}&offset={offset}'


if __name__ == '__main__':
    """
    这是封装好的知乎API.
    创建一个ZhiHu实例,将方法作为参数传入data_getter.get_data
    由data_getter判断API类型并决定如何请求
    """
    klsdaf = 'sdf'
    zhi = ZhiHu()
    print(zhi.members.followees('strangestring', 0, query_args=['following_count']))
    print(zhi.pins.info(1109795657325490176))
