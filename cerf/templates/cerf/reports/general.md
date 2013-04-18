## Interview with {{applicant}} by {{manager}} on {{started}}

{{description}}

### Summary

The exam took for __{{time_spent}}__. Total __{{applicant_count_temp}}__ took this exam, average time spent is __{{avg_time_spent_temp}}__.

{% for result in results %}
### Case{{result.position}}: {{result.name}}

This case is for {{result.level}} on {{result.type}}. The category is {{result.category}}. Coding language should be {{result.language}}.

{{result.description}}

    {{result.code}}

{% endfor %}
