import matplotlib.pyplot as plt
from glob import *
from datetime import datetime, date
from statistics import mode

#input: a list of filenames
#Return: nothing, but produces and save graphs
def produce_date_graphs(date_files):

    #Get the start dates and end dates from the files
    start_dates, end_dates = get_dates(date_files)

    #Defining earliest and latest dates to include in graphs
    earliest = date(2015,1,1)
    today = date.today()
    latest = date(2025,12,1)

    #Strip the lists for unwanted dates
    for i in range(len(start_dates)):
        if start_dates[i] > earliest:
            start_dates = start_dates[i:]
            break

    for i in range(len(end_dates)):
        if end_dates[i] > today:
            end_dates = end_dates[i:]
            break
        
    for i in range(len(end_dates)):        
        if end_dates[i] > latest:
            end_dates = end_dates[:i]
            break
            
    #Checking how many certificates issued / expired per month
    issued_monthly = monthly(start_dates)
    expires_monthly = monthly(end_dates, max_months = 40)

    #Category
    issued = 'Issue'
    expired = 'Expiration'

    #Important dates regarding Google announcements
    important_dates = [date(2016, 9, 1), date(2018, 2, 1)]

    #Generate the graphs
    certificates_figure(issued_monthly, start_dates[0], start_dates[-1], issued, important_dates)
    certificates_figure(expires_monthly, end_dates[0], end_dates[-1], expired, n = 3)



#Input: a list of filenames
#Return: two sorted lists of start dates and end dates
def get_dates(date_files):
    
    #Create lists to store information
    start_dates = []
    end_dates = []

    #Read each file with certificate dates
    for file in date_files:
        f = open(file,'r')

        #Read each line in the file
        for line in f:

            #Split the information and add it to its respective lists
            (website,start,end) = line.strip().split(":")
            start_dates.append(datetime.strptime(start, '%Y-%m-%d').date())
            end_dates.append(datetime.strptime(end, '%Y-%m-%d').date())

    #Return the dates in sorted order
    return (sorted(start_dates), sorted(end_dates))



#Input: a list of dates and number max_months (optional)
#Return: a list with number of monthly occurences
def monthly(dates, max_months = 0):

    #Calculate the number of months between start date and end date
    months = (dates[-1].year - dates[0].year)*12 + (dates[-1].month - dates[0].month) + 1

    #Create a list to count monthly occurences
    monthly_stats = [0]*months

    #Run through all dates and count occurences
    for d in dates:
        index = (d.year - dates[0].year)*12 + (d.month - dates[0].month)
        monthly_stats[index] += 1

    #Strip the list if restricted number of months
    if max_months > 0:
        return monthly_stats[:max_months]
    else:
        return monthly_stats



#Input: a list l and a number n
#Return: lists of n top elements in l and their indexes
def n_largest(l, n):

    #Creating lists to store top elements and their index
    top = [0]*n
    ind = [0]*n

    #Run throug all elements in the list l
    for i in range(len(l)):

        #Assigning temporary values
        e = l[i]
        index = -1

        #Checking if the element is greater than any
        #in the list of top elements
        for j in range(n):
            if e > top[j]:
                index = j
                break

        #If the element is bigger than any top elements,
        #then insert it in the list and replace all smaller
        if index > -1:
            for j in range(n - index):
                top[n-j-1] = top[n-j-2]
                ind[n-j-1] = ind[n-j-2]

            top[index] = e
            ind[index] = i

    #Return the n top elements in l and their indexes
    return (top, ind)
            


#Input: list of occurences per month, start date, end date, label and optional list of important dates and number n
#Return: nothing, but creates and saves graphs
def certificates_figure(monthly_stats, start, end, text, important_dates = [], n = 0):        

    #Create new figure
    fig = plt.figure()

    #Set title for figure
    fig.suptitle(text + " dates for X.509 certificates", fontsize=15, fontweight='bold')

    #Add x-axis and y-axis to the figure
    ax = fig.add_subplot(111)
    ax.set_xlabel('Months from ' + str(start.strftime("%B %Y")) + " to " + str(end.strftime("%B %Y")),fontsize=12)
    ax.set_ylabel('Number of certificates',fontsize=12)

    #Add datapoints to the figure
    ax.plot([i for i in range(1,len(monthly_stats)+1)], monthly_stats)
    
    #Add top results to graph, depending on the size of n
    if n > 0:

        #Get top elements and indexes from the list
        top,ind = n_largest(monthly_stats, n)

        #Set higth to top element
        h = top[0]

        #Add text to label
        ax.text(len(monthly_stats) - 20, h, "Most frequent:", fontsize=15)

        #Run through all n top elements, optional
        for i in range(n):

            #Find the month of the given element
            (y, m) =  divmod(start.month + ind[i], 12)
            d = date(start.year + y, m + 1, 1)

            #Print the month of the given element
            ax.text(len(monthly_stats) - 17, h*(1 - 0.1*(i+1)), "- " + str(d.strftime("%B %Y")) + ": " + str(top[i]), fontsize=15)

    #Check if there is any important dates to add to the figure
    if len(important_dates) > 0:
        for d in important_dates:

            #Find the month of the important date
            x = ((d.year - start.year)*12 + (d.month - start.month))

            #Find the top element and its index
            top,ind = n_largest(monthly_stats, 1)

            #Add name to the line of the important date
            ax.text(x - 2, top[0] - 50, d.strftime("%B %Y"), rotation = 'vertical', fontsize=12)

            #Add the line of the important date to the figure
            plt.axvline(x, color = 'k', linestyle = '--')
    
    #fig.show()
    #Save the figure as pdf and png
    fig.savefig("figures\\plot-" + text + ".pdf", dpi=150)
    fig.savefig("figures\\plot-" + text + ".png", dpi=150)

    #Close the figure
    plt.close(fig)



#Input: a list of dates, number of months (optional, set to 61)
#Return: nothing, but creates and saves graphs
def produce_length_graph(date_files, n = 61):
    
    lengths = []

    #Run through all files in the list
    for file in date_files:
        f = open(file,'r')

        #Run through all lines in the file
        for line in f:

            #Split the information, calculate the lenght and add it to the lists
            (website,start,end) = line.strip().split(":")
            s = datetime.strptime(start, '%Y-%m-%d').date()
            e = datetime.strptime(end, '%Y-%m-%d').date()
            lengths.append((e.year - s.year)*12 + (e.month - s.month))

    #Create a list to store the data
    occurrences = [0]*max(lengths)
    
    #Count the occurences of all lengths
    for l in lengths:
        occurrences[l-1] += 1

    #Strip the list for dates beyond n months    
    occurrences = occurrences[:n]

    #Create new figure
    fig = plt.figure()

    #Add title to figure
    fig.suptitle("SSL/TLS Certificate Validity", fontsize = 15, fontweight = 'bold')

    #Add x-axis and y-axis to figure
    ax = fig.add_subplot(111)
    ax.set_xlabel('Number of months the certificate is valid',fontsize=12)
    ax.set_ylabel('Number of certificates valid in $X$ months',fontsize=12)

    #Add datapoints to the figure
    ax.plot([i for i in range(1,len(occurrences)+1)], occurrences)
    
    #Add the mode to the figure
    ax.text(0.7 * len(occurrences), max(occurrences)*0.9, "Mode: " + str(mode(lengths)) + " months", fontsize = 12)

    #fig.show()
    #Save the figure as pdf and png
    fig.savefig("figures\\certificate_lengths.pdf", dpi=150)
    fig.savefig("figures\\certificate_lengths.png", dpi=150)

    #Close the figure
    plt.close(fig)
    
