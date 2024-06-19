# address-regex
At the start, I have two main goals for this project:
0. Extract the text information from invoice documents (pdfs, jpgs, pngs, etc)
0. Use regex to extract the addresses from the documents

I will begin the project by building a small collection of example invoice documents. I will choose documents with different structure: the address is on one line, the address is on two lines, there are multiple addresses, etc. I will find, learn, and apply Python libraries to extract text information from the documents. Once I can reliably extract the text information, I will work on writing a series of regex statements. The first will attempt to capture an address written on one line. The next couple will capture the first and second halves of an address. Based on the order in which I capture these groups, I will piece together the addresses. I believe that address capture can be accomplished reliably using regex.