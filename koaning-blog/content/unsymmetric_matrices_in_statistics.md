
<script type="text/javascript"
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

If you're studying statistics you may have heard that a confusion matrix $\Sigma$ for a multivariate normal distribution needs to be symmetric.

$$ f(x|m, \Sigma) = \frac{1}{\sqrt{(2\pi)^n |\Sigma|}} exp\big(-\frac{1}{2}(x-m)^T\Sigma^{-1}(x-m)\big)$$  

However, if you play around with numpy, you may get the idea that you can fill in a confusion matrix that is not symmetrical and still be able to generate random variables. 

```
import numpy as np
import matplotlib as plt 

mean = [10, 3]
nd = 10
cov = [[20, nd], [nd, 0.1]]
x, y = np.random.multivariate_normal(mean, cov, 500).T
plt.scatter(x, y, alpha = 0.5)
```

This confuses people. In this document I'll explain what is going on when a normal distribution is confronted with a non symmetrical confusion matrix. It is meant to have people appreciate the maths behind it a bit more but also as a personal reference for some linear algebra lemmas.

## Definitions 

Let's zoom in on the distribution where we are actually dealing with the confusion matrix. We will ignore the $|\Sigma|$ because you do not need it to generate the data (MCMC) or for principal component analysis.

$$ f(x|m, \Sigma) \propto exp\big(-\frac{1}{2}(x-m)^T\Sigma^{-1}(x-m)\big)$$  

Then without loss of generality I'll assume that the mean of each variable within $x$ is 0. 

$$ f(x|\Sigma) \propto exp\big(-\frac{1}{2}(x)^T\Sigma^{-1}(x)\big)$$  

We can also loose the fraction within the exponential and we'd still be proportional. 

$$ f(x|\Sigma) \propto exp\big((x)^T\Sigma^{-1}(x)\big)$$  

So what happends to a matrix when we take the exponent of it? 

## Rewriting Things 

The exponential function can be defined via;

$$ e^x = \sum_{i=0}^\infty \frac{x^i}{i!} $$ 

For a matrix, the definition is very similar. 

$$ e^X = \sum_{i=0}^\infty \frac{X^i}{i!} $$ 

From this definition we can explore two easy examples. 

#### Example 1

\\[e^I =  exp\Big(\begin{pmatrix}
1 & 0 & 0 \\\
0 & 1 & 0 \\\
0 & 0 & 1 
\end{pmatrix}\Big) = \begin{pmatrix}
e & 0 & 0 \\\
0 & e & 0 \\\
0 & 0 & e 
\end{pmatrix}\\]

#### Example 2

\\[ exp\Big(\begin{pmatrix}
1 & 0 & 0 \\\
0 & 2 & 0 \\\
0 & 0 & 3 
\end{pmatrix}\Big) = \begin{pmatrix}
e & 0 & 0 \\\
0 & e^2 & 0 \\\
0 & 0 & e^3 
\end{pmatrix}\\]

#### Example 3 

\\[ exp\Big(\begin{pmatrix}
3 & 1 \\\
1 & 2
\end{pmatrix}\Big) \approx \begin{pmatrix}
1 & 0 \\\
0 & 1
\end{pmatrix} + \begin{pmatrix}
3 & 1 \\\
1 & 2
\end{pmatrix} + \frac{1}{2}
\begin{pmatrix}
10 & 6 \\\
6 & 10
\end{pmatrix}\\ + \frac{1}{6}
\begin{pmatrix}
36 & 28 \\\
28 & 36
\end{pmatrix} + ... \\]