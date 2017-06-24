
# coding: utf-8

# # Hospital Readmissions Data Analysis and Recommendations for Reduction
# 
# ### Background
# In October 2012, the US government's Center for Medicare and Medicaid Services (CMS) began reducing Medicare payments for Inpatient Prospective Payment System hospitals with excess readmissions. Excess readmissions are measured by a ratio, by dividing a hospital’s number of “predicted” 30-day readmissions for heart attack, heart failure, and pneumonia by the number that would be “expected,” based on an average hospital with similar patients. A ratio greater than 1 indicates excess readmissions.
# 
# ### Exercise Directions
# 
# In this exercise, you will:
# + critique a preliminary analysis of readmissions data and recommendations (provided below) for reducing the readmissions rate
# + construct a statistically sound analysis and make recommendations of your own 
# 
# More instructions provided below. Include your work **in this notebook and submit to your Github account**. 
# 
# ### Resources
# + Data source: https://data.medicare.gov/Hospital-Compare/Hospital-Readmission-Reduction/9n3s-kdb3
# + More information: http://www.cms.gov/Medicare/medicare-fee-for-service-payment/acuteinpatientPPS/readmissions-reduction-program.html
# + Markdown syntax: http://nestacms.com/docs/creating-content/markdown-cheat-sheet
# ****

# In[23]:

get_ipython().magic('matplotlib inline')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import bokeh.plotting as bkp
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats.stats import pearsonr


# In[3]:

# read in readmissions data provided
hospital_read_df = pd.read_csv('data/cms_hospital_readmissions.csv')
hospital_read_df.head()


# ****
# ## Preliminary Analysis

# In[6]:

# deal with missing and inconvenient portions of data 
clean_hospital_read_df = hospital_read_df[hospital_read_df['Number of Discharges'] != 'Not Available']
clean_hospital_read_df.loc[:, 'Number of Discharges'] = clean_hospital_read_df['Number of Discharges'].astype(int)
clean_hospital_read_df = clean_hospital_read_df.sort_values('Number of Discharges')
clean_hospital_read_df.tail()


# In[7]:

# generate a scatterplot for number of discharges vs. excess rate of readmissions
# lists work better with matplotlib scatterplot function
x = [a for a in clean_hospital_read_df['Number of Discharges'][81:-3]]
y = list(clean_hospital_read_df['Excess Readmission Ratio'][81:-3])

fig, ax = plt.subplots(figsize=(8,5))
ax.scatter(x, y,alpha=0.2)

ax.fill_between([0,350], 1.15, 2, facecolor='red', alpha = .15, interpolate=True)
ax.fill_between([800,2500], .5, .95, facecolor='green', alpha = .15, interpolate=True)

ax.set_xlim([0, max(x)])
ax.set_xlabel('Number of discharges', fontsize=12)
ax.set_ylabel('Excess rate of readmissions', fontsize=12)
ax.set_title('Scatterplot of number of discharges vs. excess rate of readmissions', fontsize=14)

ax.grid(True)
fig.tight_layout()


# ****
# 
# ## Preliminary Report
# 
# Read the following results/report. While you are reading it, think about if the conclusions are correct, incorrect, misleading or unfounded. Think about what you would change or what additional analyses you would perform.
# 
# **A. Initial observations based on the plot above**
# + Overall, rate of readmissions is trending down with increasing number of discharges
# + With lower number of discharges, there is a greater incidence of excess rate of readmissions (area shaded red)
# + With higher number of discharges, there is a greater incidence of lower rates of readmissions (area shaded green) 
# 
# **B. Statistics**
# + In hospitals/facilities with number of discharges < 100, mean excess readmission rate is 1.023 and 63% have excess readmission rate greater than 1 
# + In hospitals/facilities with number of discharges > 1000, mean excess readmission rate is 0.978 and 44% have excess readmission rate greater than 1 
# 
# **C. Conclusions**
# + There is a significant correlation between hospital capacity (number of discharges) and readmission rates. 
# + Smaller hospitals/facilities may be lacking necessary resources to ensure quality care and prevent complications that lead to readmissions.
# 
# **D. Regulatory policy recommendations**
# + Hospitals/facilties with small capacity (< 300) should be required to demonstrate upgraded resource allocation for quality care to continue operation.
# + Directives and incentives should be provided for consolidation of hospitals and facilities to have a smaller number of them with higher capacity and number of discharges.

# ****
# <div class="span5 alert alert-info">
# ### Exercise
# 
# Include your work on the following **in this notebook and submit to your Github account**. 
# 
# A. Do you agree with the above analysis and recommendations? Why or why not?
#    
# B. Provide support for your arguments and your own recommendations with a statistically sound analysis:
# 
#    1. Setup an appropriate hypothesis test.
#    2. Compute and report the observed significance value (or p-value).
#    3. Report statistical significance for $\alpha$ = .01. 
#    4. Discuss statistical significance and practical significance. Do they differ here? How does this change your recommendation to the client?
#    5. Look at the scatterplot above. 
#       - What are the advantages and disadvantages of using this plot to convey information?
#       - Construct another plot that conveys the same information in a more direct manner.
# 
# 
# 
# You can compose in notebook cells using Markdown: 
# + In the control panel at the top, choose Cell > Cell Type > Markdown
# + Markdown syntax: http://nestacms.com/docs/creating-content/markdown-cheat-sheet
# </div>
# ****

# In[ ]:

# Your turn


# Question: Do you agree with the above analysis and recommendations? Why or why not?
# 
# Answer: The report provides two analysis which can be tested statistically.
# 
# There is a significant correlation between hospital capacity (number of discharges) and readmission rates.
# 
# Small hospitals (number of discharges less than 100) have lesser excess readmission rates as compared to larger hospitals (number of discharges > 1000)
# 
# We can perform a correlation and a linar regression to test the statement. The second statement can be evaluated by performing a independent (2-sample) t-test.
# 
# We can create a dataframe for small hospitals(s_hosp) having number of discharges less than(<)100. Number of discharges= 0 are neglected in our analysis.

# In[9]:

s_hosp=clean_hospital_read_df[clean_hospital_read_df['Number of Discharges'] < 100 ]
s_hosp=s_hosp[s_hosp['Number of Discharges'] !=0 ]
s_hosp.head()


# Similarly, we create a dataframe for large hospitals(l_hosp) where number of discharges is >1000.

# In[10]:

l_hosp=clean_hospital_read_df[clean_hospital_read_df['Number of Discharges'] > 1000 ]
l_hosp=l_hosp[l_hosp['Number of Discharges'] !=0 ]
l_hosp.head()


# In[11]:

s_hosp.mean()


# In[13]:

l_hosp.mean()


# We have two groups in small hospitals and large hospitals. We can perform a two sample t-test to see whether there is a difference in the excess readmission ratio for small and large hospitals.
# 
# 
# Null Hypothesis Ho: There is no difference in the excess readmission ratio for small and large hospitals.
# 
# Alternate Hypothesis Ha: There is a significant difference in the excess readmission ratio for small and large hospitals.

# In[16]:

t_stats, p_value = stats.stats.ttest_ind(s_hosp['Excess Readmission Ratio'], l_hosp['Excess Readmission Ratio'])
p_value


# Since our p-value is less than our significance level of 0.05. We reject the null hypothesis that there is no difference in the excess admission ratio between small and large hospitals.

# In[17]:

s_hosp_mean=s_hosp['Excess Readmission Ratio'].mean()
s_hosp_std=s_hosp['Excess Readmission Ratio'].std()
l_hosp_mean=l_hosp['Excess Readmission Ratio'].mean()
l_hosp_std=l_hosp['Excess Readmission Ratio'].std()


# In[20]:

cohen_d = (s_hosp_mean - l_hosp_mean) / (np.sqrt((l_hosp_std**2 + s_hosp_mean** 2) / 2))
print("cohen'd :",cohen_d)


# The value of Cohen's D is very small (0.06) which tells us that the effect of excess readmission rate in small hospitals is greater than large hospitals is very small. We can now perform a linear regression to see if there is a correlation between the number of discharges and excess readmission ratio.

# In[21]:

df= clean_hospital_read_df[clean_hospital_read_df['Number of Discharges'] != 0]


# In[22]:

stats.linregress(df['Number of Discharges'], df['Excess Readmission Ratio'])


# The R-squared value is -0.0973. This means that only about 9% of the amount of variance in our Dependent Variable     (Excess Readmission Ratio) can be explained by the variance in our Independent Variable (number of discharges). Further we can use pearson's r to check whether the two variables are related.

# In[24]:

pearsonr(df['Number of Discharges'], df['Excess Readmission Ratio'])


# Since the correlation coefficent of -0.09 is very low it shows that there is no correlation between Excess Readmission Ratio and number of discharges. Hence, the conclusion stated in the report is false.
