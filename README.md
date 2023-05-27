## Research Question

What is the relationship between emotion (emotion types, valence, and intensity) in social media content and information engagement and how moral convictions moderate the relationship?


## Social Science Significance

Social media has revolutionized the way we obtain information and shape our opinions (Cinelli et al., 2021), and it also affects our mental health (Braghieri et al., 2022) and behaviors (Kaya & Bicen, 2016). As our dependency on social media platforms grows, the effects of information on our cognition, emotions, and behaviors become more significant. Reliable, valuable, and trustworthy information should receive more attention, while misinformation diffusion should be interrupted promptly. Therefore, to maximize the benefits of high-quality information and reduce the harms of misinformation, it is crucial to understand how the audience engages with the content on social media, that is, information engagement with social media content. 


## Approaches

This study uses data scraped from Reddit. The data is collected using three sets of subreddits: 1) firearms/gunpolitics, 2) Abortiondebate/prolife/prochoice, and 3) Music/movies/MovieSuggestions, to represent gun violence, abortion, and random topics, respectively. 2 AWS Lambda functions and PRAW (Python Reddit Api Wrapper) are employed in the data collection for parallelizing the scraping from 8 subreddits [Lambda1](lambda1.py), and subsequently, parallelizing the scraping of comments to all 50 Lambda workers to reduce the overall scraping time [Lambda2](lambda2.py). The full code for scraping can be found in [rds_conn.ipynb](rds_conn.ipynb).

Each reddit post or comment has its unique ID, so duplicates are avoided. However, since some messages exclusively contained images unsuitable for this research, only messages that contained textual content were selected. The data collection process included messages from the hottest posts to the least popular posts, encompassing both the posts themselves and their subsequent comments. To facilitate scalable and shareable storage, the posts and comments were stored in separate AWS RDS tables.

For each post, the following information was collected: the subreddit it belonged to, the unique ID, the title, the score (calculated as the number of upvotes minus the number of downvotes), the post URL, the number of comments, the body of the message, and the number of upvotes. Similarly, for each comment, the study gathered the subreddit it belonged to, the score (matching that of posts), the body of the message, the URL of the post it was associated with, and the unique comment ID.

Before proceeding with data analysis, certain preprocessing steps were implemented. Specifically, message bodies labeled as "[deleted]," messages containing emails and/or other URLs, and pinned messages regarding rules were removed. This preprocessing aimed to minimize potential influences on the subsequent analysis and classification of emotions.

From data analysis in [](), we have found that 

Additionally, we used Spark NLP to classify texts, including post bodies, post titles, and comment bodies, to 4 emotions, including joy, sadness, fear, and surprise. Spark NLP offers convenient access to pre-trained models and pipelines for this purpose ("Spark NLP"). When it comes to emotion classification, Spark NLP employs a neural network model that converts the text into word embeddings and subsequently assigns one of the four emotions as the output.

Finally, the project information and analysis results is deployed using flask on the AWS Elastic Beanstalk, which allows automatic scaling up and down based on demand and also increases its availability and fault tolerance as the web application is deployed across multiple availability zones ("Website & Web App Deployment—AWS Elastic Beanstalk—AWS"). The website can be accessed at Reddit-vis-env.eba-bmeifumb.us-east-1.elasticbeanstalk.com. 

## Discussion

In our study, it is important to acknowledge certain limitations.

Firstly, the rate limit of Reddit and API restrictions. It takes a long time to scrape messages due to Reddit’s rate limiting on accounts even though parallel scraping is employed. In addition, the API connection stopped over five minutes, so we were only able to get a sample of the posts and comments from the 8 subreddits.  

Secondly, we did not take into account the potential influence of subreddit moderators on the emotion analysis results. This is due to the lack of a direct method in PRAW (Python Reddit API Wrapper) to map moderator IDs to their corresponding names. As a result, we were unable to identify and exclude messages sent by moderators from our analysis.

Thirdly, the presence of bots on Reddit is another factor that could potentially affect the analysis of emotions. Bots can generate automated messages, which may not accurately represent genuine user sentiments. Although we did not specifically address the issue of bot messages in our study, it is a valid concern that warrants further research. Future studies could focus on developing methods to identify and filter out bot-generated content to reduce their impact on the analysis results. 

Lastly, it is important to note that the specific algorithm used in the pre-trained Spark NLP emotion classification model remains unknown. Consequently, we lack insights into how the model precisely classifies texts into specific emotions. While neural network models typically exhibit superior performance compared to traditional machine learning NLP models, we cannot guarantee error-free performance from the model employed in our study. Furthermore, it is worth mentioning that the emotion classification model utilized does not include a category for the fundamental emotion of "anger," which may seem peculiar. This omission of such a basic emotion raises questions and could potentially impact the comprehensiveness and accuracy of the emotion analysis results.


## References
- Braghieri, L., Levy, R., & Makarin, A. (2022). Social Media and Mental Health. American Economic Review, 112(11), 3660–3693. https://doi.org/10.1257/aer.20211218
- Cinelli, M., De Francisci Morales, G., Galeazzi, A., Quattrociocchi, W., & Starnini, M. (2021). The Echo Chamber Effect on social media. Proceedings of the National Academy of Sciences, 118(9). https://doi.org/10.1073/pnas.2023301118
- Kaya, T., & Bicen, H. (2016). The effects of social media on students’ behaviors; Facebook as a case study. Computers in Human Behavior, 59, 374–379. https://doi.org/10.1016/j.chb.2016.02.036 
- Spark NLP: State-of-the-Art Natural Language Processing. (2023). [Scala]. John Snow Labs. https://github.com/JohnSnowLabs/spark-nlp (Original work published 2017)
- Website & Web App Deployment—AWS Elastic Beanstalk—AWS. (n.d.). Amazon Web Services, Inc. Retrieved May 26, 2023, from https://aws.amazon.com/elasticbeanstalk/



## Divion of Labor:
- Yingzi Jin: data processing and analyzing (including EDA, classification, and statistical analysis) using PySpark
- Ruoyi Wu: parallel data collection, scalable deployment of visualization

