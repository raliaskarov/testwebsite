from flask import Flask, render_template

app = Flask (__name__)

@app.route('/plot/')
def plot():
    #preparing data
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start=datetime.datetime(2020,1,1)
    end=datetime.datetime(2021,8,5)
    df=data.DataReader(name="HOLN.SW",data_source="yahoo",start=start,end=end)

    def price_direction(c,o):
        if c>o:
            value="I"
        elif c<o:
            value="D"
        else:
            value="E"
        return value
    df["Status"]=[price_direction(c,o) for c, o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Open-df.Close)

    #plotting chart
    p=figure(x_axis_type='datetime',
            width=1000,
            height=300,
            sizing_mode="scale_width")
    p.title="Chart"
    p.grid.grid_line_alpha=0.3

    hours_12=12*60*60*1000

    p.segment(df.index,
            df.High,
            df.index,
            df.Low,
            line_color="black")
    #increase bars
    p.rect(df.index[df.Status=="I"],
        df.Middle[df.Status=="I"],
        hours_12,
        df.Height[df.Status=="I"],
        fill_color="#33CC33",
        line_color="#33CC33")
    #decrease bars
    p.rect(df.index[df.Status=="D"],
        df.Middle[df.Status=="D"],
        hours_12,
        df.Height[df.Status=="D"],
        fill_color="#FF4500",
        line_color="#FF4500")
    #extract links and js
    script1, div1 = components(p)
    cdn_js=CDN.js_files
    return render_template("plot.html",
                            script1=script1,
                            div1=div1,
                            cdn_js=cdn_js[0])

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)