# movie_recommend_system
data: derive from movie preferance questionnare of 18fall CSE250 students
# model: Hidden Markov Model
![model_pictures](https://github.com/aryaye/movie_recommend_system/blob/master/pictures/model_image.PNG)  
Z is hidden variables, for each student, there is a unique distrubution `P(Z=i|student_t)`  
#### In this program, the data contians the {Student_t, R_t}t  
## Loglikelihood  
the likelihood of student_t's rating is  
![likelihood_pictures](https://github.com/aryaye/movie_recommend_system/blob/master/pictures/formular1.PNG)  
Ωt denote the set of movies seen(and hence rated) by student_t
## EM_estimator  
#### E-step:  
E-step of this model is to comupte
For each student, the posterior probability that she or he corresponds to particular type of movie-goer, show that:  
![E_step_pictures](https://github.com/aryaye/movie_recommend_system/blob/master/pictures/estimator_formular1.PNG)  
#### M-step:  
M-step of the model is to re-estimate the probabilities P(Z=i) and P(Rj=1|Z=i) that define the `CPTs` of the belief network.   
As shorthand, let  
![shorthands_pictures](https://github.com/aryaye/movie_recommend_system/blob/master/pictures/formular2.PNG)  
after E-step compute ρit, we can update `CPTs`  
![M_steps_pictures](https://github.com/aryaye/movie_recommend_system/blob/master/pictures/estimator_formular2.PNG)  
## Recommend System  
Recommend a unseen movie from the movie student_t have saw by the criterion  
![recommend_pictures](https://github.com/aryaye/movie_recommend_system/blob/master/pictures/recommend.PNG)  
the more the left-hand probability is, the more likely the student_t will like this movie.
