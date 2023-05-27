# Large-Scale Computing Final Project: 
# The Effect of Emotion in Social Media Content on Information Engagement: Reddit Analysis

## Research Question

What is the relationship between emotion (emotion types, valence, and intensity) in social media content and information engagement and how moral convictions moderate the relationship?


## Social Science Significance

Social media has revolutionized the way we obtain information and shape our opinions (Cinelli et al., 2021), and it also affects our mental health (Braghieri et al., 2022) and behaviors (Kaya & Bicen, 2016). As our dependency on social media platforms grows, the effects of information on our cognition, emotions, and behaviors become more significant. Reliable, valuable, and trustworthy information should receive more attention, while misinformation diffusion should be interrupted promptly. Therefore, to maximize the benefits of high-quality information and reduce the harms of misinformation, it is crucial to understand how the audience engages with the content on social media, that is, information engagement with social media content. 

### Information Engagement

Information engagement, or content engagement, defined by Schreiner et al. (2019), refers to the quantifiable interaction of individuals with a piece of information without implying any connection to behavior antecedents such as attitudes, behavioral intentions, or even neurophysiological. In the context of social media, information engagement is mainly represented as at least one of the following metrics: liking (Swani et al., 2013), sharing (Nelson-Field et al., 2013; Stieglitz & Dang-Xuan, 2013), or commenting on a social media post (de Vries et al., 2012; Stieglitz & Dang-Xuan, 2012; Schreiner et al., 2019). The forms of these metrics are platform-dependent.

### Moral Conviction

Moral conviction is defined as "the belief that a given attitude is a reflection of one's core feelings or beliefs about fundamental issues of right and wrong" (Skitka et al., 2021). Topics such as abortion, capital punishment, gun control, immigration, and same-sex marriage are considered to be associated with strong moral convictions (Skitka et al., 2021). Conversely, topics related to personal preferences, such as favorite movies or music, which do not conform to the definition of moral conviction, are regarded with low or no moral conviction.

Moral conviction is linked to various emotions, encompassing those directly connected to the issue that evokes moral conviction (Skitka & Wisneski, 2011). Additionally, it involves self-relevant emotions, such as the anticipation of feeling proud when actively participating in political matters and the anticipation of guilt when failing to do so (Morgan, 2011; Skitka et al., 2017). 

When challenged, these convictions may lead to negative emotions and make it difficult for individuals to consider different perspectives (Zaal et al., 2015). Individuals with higher moral convictions were less likely to engage in perspective-taking and showed a reduced willingness to compromise on moral issues (Skitka et al., 2021). Conversely, affirmation of these convictions may generate positive emotions that reinforce beliefs and identity, suggesting the possibility that moral conviction may moderate the relationship between emotion and information engagement.



## Approaches

This study uses data scraped from Reddit. The data is collected using three sets of subreddits: 1) firearms/gunpolitics, 2) Abortiondebate/prolife/prochoice, and 3) Music/movies/MovieSuggestions, to represent gun violence, abortion, and random topics, respectively. 2 AWS Lambda functions and PRAW (Python Reddit Api Wrapper) are employed in the data collection for parallelizing the scraping from 8 subreddits **[Lambda1](lambda1.py)**, and subsequently, parallelizing the scraping of comments to all 50 Lambda workers to reduce the overall scraping time **[Lambda2](lambda2.py)**. The full code for scraping can be found in **[rds_conn.ipynb](rds_conn.ipynb)**.

Each reddit post or comment has its unique ID, so duplicates are avoided. However, since some messages exclusively contained images unsuitable for this research, only messages that contained textual content were selected. The data collection process included messages from the hottest posts to the least popular posts, encompassing both the posts themselves and their subsequent comments. To facilitate scalable and shareable storage, the posts and comments were stored in separate AWS RDS tables.

For each post, the following information was collected: the subreddit it belonged to, the unique ID, the title, the score (calculated as the number of upvotes minus the number of downvotes), the post URL, the number of comments, the body of the message, and the number of upvotes. Similarly, for each comment, the study gathered the subreddit it belonged to, the score (matching that of posts), the body of the message, the URL of the post it was associated with, and the unique comment ID.

Before proceeding with data analysis, certain preprocessing steps were implemented. Specifically, message bodies labeled as "[deleted]," messages containing emails and/or other URLs, and pinned messages regarding rules were removed. This preprocessing aimed to minimize potential influences on the subsequent analysis and classification of emotions.

From data analysis in **[]()**, we have found that 

Additionally, we used Spark NLP to classify texts, including post bodies, post titles, and comment bodies, to 4 emotions, including joy, sadness, fear, and surprise. Spark NLP offers convenient access to pre-trained models and pipelines for this purpose ("Spark NLP"). When it comes to emotion classification, Spark NLP employs a neural network model that converts the text into word embeddings and subsequently assigns one of the four emotions as the output.

Finally, the project information and analysis results is deployed using flask on the AWS Elastic Beanstalk, which allows automatic scaling up and down based on demand and also increases its availability and fault tolerance as the web application is deployed across multiple availability zones ("Website & Web App Deployment—AWS Elastic Beanstalk—AWS"). The website can be accessed at **Reddit-vis-env.eba-bmeifumb.us-east-1.elasticbeanstalk.com**. 

## Discussion

In our study, it is important to acknowledge certain limitations.

Firstly, the rate limit of Reddit and API restrictions. It takes a long time to scrape messages due to Reddit’s rate limiting on accounts even though parallel scraping is employed. In addition, the API connection stopped over five minutes, so we were only able to get a sample of the posts and comments from the 8 subreddits. 

Secondly, we did not take into account the potential influence of subreddit moderators on the emotion analysis results. This is due to the lack of a direct method in PRAW (Python Reddit API Wrapper) to map moderator IDs to their corresponding names. As a result, we were unable to identify and exclude messages sent by moderators from our analysis.

Thirdly, the presence of bots on Reddit is another factor that could potentially affect the analysis of emotions. Bots can generate automated messages, which may not accurately represent genuine user sentiments. Although we did not specifically address the issue of bot messages in our study, it is a valid concern that warrants further research. Future studies could focus on developing methods to identify and filter out bot-generated content to reduce their impact on the analysis results. 

Lastly, it is important to note that the specific algorithm used in the pre-trained Spark NLP emotion classification model remains unknown. Consequently, we lack insights into how the model precisely classifies texts into specific emotions. While neural network models typically exhibit superior performance compared to traditional machine learning NLP models, we cannot guarantee error-free performance from the model employed in our study. Furthermore, it is worth mentioning that the emotion classification model utilized does not include a category for the fundamental emotion of "anger," which may seem peculiar. This omission of such a basic emotion raises questions and could potentially impact the comprehensiveness and accuracy of the emotion analysis results.


## References
- Braghieri, L., Levy, R., & Makarin, A. (2022). Social Media and Mental Health. American Economic Review, 112(11), 3660–3693. https://doi.org/10.1257/aer.20211218
- Cinelli, M., De Francisci Morales, G., Galeazzi, A., Quattrociocchi, W., & Starnini, M. (2021). The Echo Chamber Effect on social media. Proceedings of the National Academy of Sciences, 118(9). https://doi.org/10.1073/pnas.2023301118
- De Vries, L., Gensler, S., & Leeflang, P. S. H. (2012). Popularity of brand posts on Brand Fan Pages: An investigation of the effects of social media marketing. Journal of Interactive Marketing, 26(2), 83–91. https://doi.org/10.1016/j.intmar.2012.01.003
- Kaya, T., & Bicen, H. (2016). The effects of social media on students’ behaviors; Facebook as a case study. Computers in Human Behavior, 59, 374–379. https://doi.org/10.1016/j.chb.2016.02.036 
- Morgan, G.S. (2011). Toward a Model of Morally Motivated Behavior: Investigating Mediators of the Moral Conviction-Action Link.
- Nelson-Field, K., Riebe, E., & Newstead, K. (2013). The emotions that drive viral video. Australasian Marketing Journal, 21(4), 205–211. https://doi.org/10.1016/j.ausmj.2013.07.003
- Schreiner, M., Fischer, T., & Riedl, R. (2019). Impact of content characteristics and emotion on behavioral engagement in social media: Literature Review and research agenda. Electronic Commerce Research, 21(2), 329–345. https://doi.org/10.1007/s10660-019-09353-8
- Skitka, L. J., Bauman, C. W., & Mullen, E. (2021). Moral conviction. Annual Review of Psychology, 72, 1-24.
- Spark NLP: State-of-the-Art Natural Language Processing. (2023). [Scala]. John Snow Labs. https://github.com/JohnSnowLabs/spark-nlp (Original work published 2017)
- Stieglitz, S., & Dang-Xuan, L. (2013). Emotions and Information Diffusion in Social Media—Sentiment of Microblogs and Sharing Behavior. Journal of Management Information Systems, 29(4), 217-248. doi: 10.2753/MIS0742-1222290408
- Swani, K., Milne, G., & P. Brown, B. (2013). Spreading the word through likes on Facebook. Journal of Research in Interactive Marketing, 7(4), 269–294. https://doi.org/10.1108/jrim-05-2013-0026 
- Website & Web App Deployment—AWS Elastic Beanstalk—AWS. (n.d.). Amazon Web Services, Inc. Retrieved May 26, 2023, from https://aws.amazon.com/elasticbeanstalk/


## Divion of Labor:
- Yingzi Jin: data processing and analyzing (including EDA, classification, and statistical analysis) using PySpark
- Ruoyi Wu: parallel data collection, scalable deployment of visualization

