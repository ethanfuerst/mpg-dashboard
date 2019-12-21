def mpg_insights(df):
    print()
    print(df.name + ':')
    print("Total miles: " + str(round(sum(df['miles']), 2)) + " miles")
    print("Total spent on gas: $" + str(round(sum(df['dollars']), 2 )))
    print("Total gallons pumped: " + str(round(sum(df['gallons']), 2)) + " gallons")
    print("Miles per gallon: " + str(round(sum(df['miles'])/sum(df['gallons']), 2)))
    print("Average cost of one gallon of gas: $" + str(round(sum(df['dollars'])/sum(df['gallons']), 2)))
    print("Cost to go one mile: $" + str(round(sum(df['dollars'])/sum(df['miles']), 2)))
