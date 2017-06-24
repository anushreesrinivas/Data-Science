
# coding: utf-8

# # Examining Racial Discrimination in the US Job Market
# 
# ### Background
# Racial discrimination continues to be pervasive in cultures throughout the world. Researchers examined the level of racial discrimination in the United States labor market by randomly assigning identical résumés to black-sounding or white-sounding names and observing the impact on requests for interviews from employers.
# 
# ### Data
# In the dataset provided, each row represents a resume. The 'race' column has two values, 'b' and 'w', indicating black-sounding and white-sounding. The column 'call' has two values, 1 and 0, indicating whether the resume received a call from employers or not.
# 
# Note that the 'b' and 'w' values in race are assigned randomly to the resumes when presented to the employer.

# <div class="span5 alert alert-info">
# ### Exercises
# You will perform a statistical analysis to establish whether race has a significant impact on the rate of callbacks for resumes.
# 
# Answer the following questions **in this notebook below and submit to your Github account**. 
# 
#    1. What test is appropriate for this problem? Does CLT apply?
#    2. What are the null and alternate hypotheses?
#    3. Compute margin of error, confidence interval, and p-value.
#    4. Write a story describing the statistical significance in the context or the original problem.
#    5. Does your analysis mean that race/name is the most important factor in callback success? Why or why not? If not, how would you amend your analysis?
# 
# You can include written notes in notebook cells using Markdown: 
#    - In the control panel at the top, choose Cell > Cell Type > Markdown
#    - Markdown syntax: http://nestacms.com/docs/creating-content/markdown-cheat-sheet
# 
# 
# #### Resources
# + Experiment information and data source: http://www.povertyactionlab.org/evaluation/discrimination-job-market-united-states
# + Scipy statistical methods: http://docs.scipy.org/doc/scipy/reference/stats.html 
# + Markdown syntax: http://nestacms.com/docs/creating-content/markdown-cheat-sheet
# </div>
# ****

# In[14]:

import pandas as pd
import numpy as np
from scipy import stats
import math


# In[6]:

data = pd.io.stata.read_stata('data/us_job_market_discrimination.dta')


# In[3]:




# In[4]:

data.head()


# Question: What are the null and alternate hypotheses?
# Answer: Our null hypothesis Ho is that the proportion of callbacks for black-sounding names is equal to the proportion of callbacks for white-sounding names.
# 
# Alternate hyothesis Ha: The proportion of callbacks for black-sounding names is not equal to the proportion of callbacks for white-sounding names.

# In[7]:

n_black= len(data[data.race == 'b'])
n_white= len(data[data.race == 'w'])


# In[8]:

# number of callbacks for black-sounding names
sum_black=sum(data[data.race=='b'].call)
sum_white=sum(data[data.race=='w'].call)


# In[10]:

prop_black= sum_black/n_black
prop_black


# In[11]:

prop_white= sum_white/n_white
prop_white


# In[12]:

diff_prop=prop_white-prop_black
diff_prop


# In[15]:

SE_black = (prop_black * (1 - prop_black)) / n_black
SE_white = (prop_white * (1 - prop_white)) / n_white
SE = math.sqrt(SE_black + SE_white)
SE


# Compute margin of error, confidence interval, and p-value.
# 
# At 95% confidence interval we take the critical z-value to be 1.96 to calculate the margin error (ME). Confidence interval would range from diff_prop- ME to diff_prop+ME.

# In[16]:

ME=1.96*SE
ME


# In[17]:

CI=[diff_prop-ME,diff_prop+ME]
CI


# We can now calculate the z-score as the difference of the difference between the two proportions (diff_prop) and our assumed value of the mean i.e. 0 (since u_black=u_white=0) divided by the Standard error.

# In[18]:

z=(diff_prop-0)/SE
z


# Question: Discuss statistical significance.
# 
# Answer: Since the value of z is greater than the critical values of 1.96 at 5% significance level, we can say that this value of 4.115 is even less probable than 1.96. Therefore the p-value is even less than 5%. As p-value is less than 0.05 , we reject our null hypothesis that the proportions of callbacks for black-sounding names is equal to the proportion of callbacks for white-sounding names.
# 
# Therefore we can go for our alternate hypothesis that people with white-sounding names are more likely to have callbacks than people with black-sounding names.
# 
