
import plotly
import plotly.plotly as py
import plotly.figure_factory as ff

class Chart(object):

    def plott_example(self):
        df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
              dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
              dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')]

        fig = ff.create_gantt(df)
        plotly.offline.plot(fig, filename='gantt-simple-gantt-chart')

    def local_gantt(self, steps, jupyter=False):
        """
        Gantt chart local visualization,
        uses list of Step class objects
        to create info
        :param steps:
        :return:
        """
        if jupyter is True:
            plotly.offline.init_notebook_mode(connected=True)
        df = []
        for step in steps:
            dd = dict(Task=step.step_name,
                      Start=step.step_start_time,
                      Finish=step.timeback
                      )
            df.append(dd)
        fig = ff.create_gantt(df,
                              title='Combined Schedule',
                              bar_width=0.4,
                              showgrid_x=True,
                              showgrid_y=True)
        plotly.offline.plot(fig, filename='local-gantt-chart.html')

