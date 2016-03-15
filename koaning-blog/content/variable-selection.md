Title: Variable Selection in Machine Learning
Date: 2014-12-18

<script type="text/javascript"
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

<p> I've had a discussion with a colleague on the selection of variables in a model. The discussion boils down to the following question: </p>

<pre>Which is better? 
- supply all the variables that you have into the model and risk overfitting 
- start out small and add values to make the model more and more complex?</pre>

 <p> You should always use a test set to determine the performance of your models and you should apply strategies to prevent it from overfitting, but starting our small and growing the model brings inherit bias into the model. In this document I will provide a mathematical proof of what might be dangerous of this approach.</p>

<h3>Linear Algrebra/Regression Primer </h3>

<p>Warning, this document is heavy on math. In this document I've assumed that you have some remembrance of college level linear algebra. The following equations should feel readable to you:</p>

\begin{aligned}
M_x & = I_n - X(X'X)^{-1}X' \\\
M_x X & = I_nX - X(X'X)^{-1}X'X \\\
& = X - XI_n\\\
& = 0 
\end{aligned}

<p> From statistics you should hopyfully feel familiar with the following: </p>
 
\begin{aligned}
Y & = X\beta + \epsilon  \text{        where    } \epsilon \sim N(0,\sigma) \\\
\hat{\beta} & = (X'X)^{-1} X'Y \\\
\mathbb{E}(\hat{\beta} ) & = \mathbb{E}\big((X'X)^{-1} X'Y)\big)
\end{aligned}

<h3>Proof</h3>

<p>I am going to proove that for linear models you will introduce bias if you use few variables and include more and more as you are building a model and that this will not happen when you start with a lot of variables and reduce. For each case I will show what goes wrong in terms of the expected value of the $\beta$ variables.</p>

A few things on notation, I will refer to the following linear regression formula:

<br> 

$$ Y = X_1\beta_1 + X_2\beta_2 + \epsilon $$ 

In this notation, $X_1,X_2$ are matrices containing data, not vectors, such that $\beta_1,\beta_2$ are matrices as well.

<br>
<h4>Small to Large Problems</h4>

<p>Suppose that the true model is given through:</p>

$$ Y = X_1\beta_1 + X_2\beta_2 + \epsilon $$ 

<p> If we start out with a smaller model, say by only looking at $\beta_1$ we would estimate for $ Y = X_1\beta_1 + \epsilon$ while the whole model should be $ Y = X_1\beta_1 + X_2\beta_2 + \epsilon $. Then our expected value of $\beta_1$ can be derived analytically. </p>


\begin{aligned}
\mathbb{E}(\beta_1) & = \mathbb{E}\big((X_1'X_1)^{-1} X_1'Y)\big)\\\
& = \mathbb{E}\Big((X_1'X_1)^{-1} X_1'\big(X_1\beta_1 + X_2\beta_2 + \epsilon\big)\Big)\\\
& = \mathbb{E}\Big((X_1'X_1)^{-1} X_1'X_1\beta_1 + (X_1'X_1)^{-1} X_1'X_2\beta_2 + (X_1'X_1)^{-1} X_1'\epsilon\big)\Big)\\\
& = \mathbb{E}\Big(\beta_1 + (X_1'X_1)^{-1} X_1'X_2\beta_2 + (X_1'X_1)^{-1} X_1'\epsilon\big)\Big)  \\\
& = \beta_1 + (X_1'X_1)^{-1} X_1'X_2\beta_2 + (X_1'X_1)^{-1} X_1'\mathbb{E}(\epsilon) \\\
& = \beta_1 + (X_1'X_1)^{-1} X_1'X_2\beta_2 \\\
& \ne \beta_1
\end{aligned}

<p> So our estimate of $\beta_1$ is biased. This holds for every subset of variables $\{\beta_1, \beta_2\}$ that make up $/beta$. </p>

<h4>Large to Small Solution</h4>

<p> Suppose that the true model is given through:</p>

$$ Y = X_1\beta_1 + \epsilon $$ 

If we start out with a larger model, say by including some parameters $\beta_2$ as well while they do not have any influence on the model then we will initially estimate a wrong model $Y = X_1\beta_1 + X_2\beta_2 + \epsilon$. 

<br><br><br>

<h4>A lemma in between</h4>

Let's define a matrix $M_{X_1} = I_n -X_1(X_1'X_1)^{-1}X_1'$. We can use this matrix to get an estimate of $\beta_2$. 

Start out with the original formula. 

\begin{aligned}
M_{X_1}Y & = M_{X_1}X_1\beta_1 + M_{X_1}X_2\beta_2 + M_{X_1}\epsilon \\\
M_{X_1}Y & = M_{X_1}X_2\beta_2 + \epsilon \\\
X_2'M_{X_1}Y & = X_2'M_{X_1}X_2\beta_2 + X_2'\epsilon \\\
X_2'M_{X_1}Y & = X_2'M_{X_1}X_2\beta_2 \\\
\beta_2 & = ( X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}Y \\\
\end{aligned}

Notice that $M_{X_1}X_1 = 0$ and that $M_{X_1}\epsilon = \epsilon$ because of the definition while $X_2\epsilon = 0$ because $\epsilon$ is normally distributed around zero and orthogonal to any of the explanatory variables. 

<h3> The derivation for large to small </h3>

With this definition of $\beta_2$ we can analyse it to confirm that it should not converge to any other value than zero. 

\begin{aligned}
\mathbb{E}(\beta_2) & = \mathbb{E}\big(( X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}Y\big) \\\
& = \mathbb{E}\big(( X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}\big(X_1\beta_1 + \epsilon\big)\big) \\\
& = \mathbb{E}\big(( X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}X_1\beta_1 + ( X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}\epsilon\big) \\\
& = \mathbb{E}\big(( X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}\epsilon\big) \\\
& = ( X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}\mathbb"t{E}(\epsilon) \\\
& = 0
\end{aligned}

<p> Notice that $ ( X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}X_1\beta_1 = 0 $ because $ M_{X_1}X_1 = 0 $. So we see that $\beta_2$ is correctly estimated, what about $\beta_1$? </p>

\begin{aligned}
\mathbb{E}(\beta_1) & = \mathbb{E}\big((X_1'X_1)^{-1} X_1'Y)\big)\\\
& = \mathbb{E}\Big((X_1'X_1)^{-1} X_1'\big(X_1\beta_1 + \epsilon\big)\Big)\\\
& = \mathbb{E}\Big(\beta_1 + (X_1'X_1)^{-1} X_1'\epsilon\Big)\\\
& = \beta_1
\end{aligned}



<p> So in this case we would remove the variables $\beta_2$ that are not of influence while our estimate of $\beta_1$ does not have any bias. This is exactly what we want. </p>

<h3>Conclusion</h3>

I've shown that by starting only a few variables and then adding them to the model has a bias risk in linear models. It should be said that you are still not without risk, I merely want to point out a risk that I am weary for. 

For other (non linear) models you might expect the similar situation. A model will try to use any correlation that it can find in the data to find a pattern. To prevent this it might be a good tactic to start with all variables and to use less and less variables until overfitting is no longer an issue and all variables in the model are significant. This way you might prevent assigning too much predictive power to a variable that might need to be reallocated to a variable that isn't included.