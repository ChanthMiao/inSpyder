# -*- coding: utf-8 -*-

# from orm.sql import manager
import numpy as np
import matplotlib.pyplot as plt
import time
import jieba
from wordcloud import WordCloud
from orm.sql import manager


def PostingTimeDistribution(picDataList: list, fid=None, display=False):
    utcTimeList = []
    postingTimeList = []
    for line in picDataList:
        utcTimeList.append(line[0])
    for times in utcTimeList:
        mytime = time.localtime(float(times))
        postingTimeList.append(
            int(int(time.strftime("%H%M%S", mytime)) / 10000))
    frequencyList = []
    for iter in range(24):
        frequencyList.append(0)
    for element in postingTimeList:
        frequencyList[element] += 1
    plt.figure(fid)
    plt.xticks(postingTimeList)
    plt.plot(frequencyList)
    plt.xlabel('posting time')
    plt.ylabel('frequency')
    plt.title('Posting Time Distribution')
    if display:
        plt.show()


def PostFrenquencyAndFollower(userDataList: list, fid=None, display=False):
    frequencyList = []
    followerList = []
    for line in userDataList:
        frequencyList.append(int(line[0]))
    for line in userDataList:
        followerList.append(int(line[2]))
    plt.figure(fid)
    plt.xticks(frequencyList.sort())
    plt.plot(followerList)
    plt.xlabel('post frequency')
    plt.ylabel('follower')
    plt.title('Posting frequency and followers')
    if display:
        plt.show()


def FollowingAndFollower(userDataList: list, fid=None, display=False):
    followingList = []
    followerList = []
    for line in userDataList:
        followingList.append(int(line[1]))
    for line in userDataList:
        followerList.append(int(line[2]))
    plt.figure(fid)
    plt.xticks(followingList.sort())
    plt.plot(followerList)
    plt.xlabel('following')
    plt.ylabel('follower')
    plt.title('Followings & followers')
    if display:
        plt.show()


def UserProileKeyWords(userDataList: list, fid=None, display=False):
    text = ''
    for line in userDataList:
        text += line[3]
    cut_text = jieba.cut(text)
    result = "/".join(cut_text)
    wc = WordCloud(
        background_color='white',
        width=800,
        height=600,
        max_font_size=80,
        max_words=1000)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')
    wc.generate(result)
    wc.to_file(r"figures/wordcloud.png")  # 按照设置的像素宽高度保存绘制好的词云图
    # 4、显示图片
    plt.figure(fid)
    plt.imshow(wc)  # 以图片的形式显示词云
    plt.axis("off")
    if display:
        plt.show()


def PostingTimeAndComments(picDataList: list, fid=None, display=False):
    utcTimeList = []
    postingTimeList = []
    for line in picDataList:
        utcTimeList.append(line[0])
    for times in utcTimeList:
        mytime = time.localtime(float(times))
        postingTimeList.append(
            int(int(time.strftime("%H%M%S", mytime)) / 10000))
    commentList = []
    for line in picDataList:
        commentList.append(int(line[1]))
    plt.figure(fid)
    plt.xticks(np.arange(0, 24, 1))
    plt.yticks(np.arange(0, len(commentList), len(commentList) / 15))
    plt.scatter(postingTimeList, commentList, s=30, marker='o', alpha=0.7)
    plt.xlabel('posting time')
    plt.ylabel('comment')
    plt.title('Posting time and comments')
    if display:
        plt.show()


def FollowerAndLike(userDataList: list,
                    picDataList: list,
                    fid=None,
                    display=False):
    likeList = []
    followerList = []
    for line in userDataList:
        followerList.append(int(line[1]))
    for line in picDataList:
        likeList.append(int(line[2]))
    plt.figure(fid)
    plt.xticks(followerList.sort())
    plt.plot(likeList)
    plt.xlabel('follower')
    plt.ylabel('like')
    plt.title('Followers & likes')
    if display:
        plt.show()


if __name__ == "__main__":
    userDataList = []
    picDataList = []
    manager = manager("postgresql://inspyder:No996icu@127.0.0.1:5432/insdata")
    userDataList = manager.get_userless_data()
    picDataList = manager.get_idless_data()
    manager.close()
    # 时间分布测试Okay
    PostingTimeDistribution(picDataList, "Posting Time Distribution")
    # 发帖数-关注数量分布测试Okay
    PostFrenquencyAndFollower(userDataList, "Post Frenquency-Follower")
    # 关键词云图生成测试Okay
    UserProileKeyWords(userDataList, "wordcloud")
    # 关注-被关注数量分布测试Okay
    FollowingAndFollower(userDataList, "Following-Follower")
    # 被关注数-点赞数分布测试Okay
    FollowerAndLike(userDataList, picDataList, "Follower-Like")
    # 发布时间-评论数分布测试Okay
    PostingTimeAndComments(picDataList, "Posting Time-Comments")
    # disyplay all.
    plt.show()
