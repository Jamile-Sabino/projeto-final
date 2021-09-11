#!/usr/bin/env python
# coding: utf-8

# In[34]:


import requests as r


# In[35]:


url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)


# In[36]:


resp.status_code


# In[37]:


raw_data = resp.json()


# In[38]:


raw_data[0]


# In[39]:


final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'], obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])


# In[40]:


final_data.insert(0,['confirmados', 'obitos', 'recuperados', 'ativos', 'data'])
final_data


# In[41]:


CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4
 


# In[42]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]


# In[43]:


final_data


# In[44]:


import datetime as dt
import csv


# In[45]:


with open('brasil-covid.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)


# In[46]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], '%Y-%m-%d' )


# In[47]:


final_data


# In[48]:


def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
        return datasets
    else:
        return [
            {
                'label': labels[0],
                'data': y
            }
        ]
        


# In[49]:


def set_title(title = ''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return {
        'title': title,
        'display': display
    }


# In[50]:


def create_chart(x, y, labels, kind = 'bar', title= ''):
    
    datasets = get_datasets(y, labels)
    options = set_title(title)
    
    
    chart = {
        'type': kind,
        'data': {
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }
    
    return chart


# In[51]:


def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content


# In[52]:


def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)


# In[53]:


from PIL import Image
from IPython.display import display


# In[65]:


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


# In[67]:


y_data_1 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[CONFIRMADOS])
    
y_data_2 = []
for obs in final_data[1::10]:
    y_data_2.append(obs[RECUPERADOS])
    
labels = ['Confirmados', 'Recuperados']

x = []
for obs in  final_data[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))
    
chart = create_chart(x, [y_data_1, y_data_2], labels, title = 'Gráfico confirmados vc recuperados')
chart_content = get_api_chart(chart)
save_image('meu-primeiro-grafico.png', chart_content)
display_image('meu-primeiro-grafico.png')
    


# In[68]:


from urllib.parse import quote


# In[69]:


def get_api_qrcode(link):
    text = quote(link) #parsing do link para url
    url_base = 'https://quickchart.io/qr'
    resp = r.get(f'{url_base}?text={text}')
    return resp.content


# In[73]:


url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png ', get_api_qrcode(link))
display_image('qr-code.png')


# In[ ]:




