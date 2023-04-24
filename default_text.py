default_text1 = "This Agreement shall be governed by and interpreted under the laws of the State of Delaware without regard to its conflicts of law provisions."
default_text2 = "This agreement will be governed by and must be construed in accordance with the laws of the State of Israel."
default_text3 = """This agreement ("Agreement") is made and entered into on this 14th day of April, 2023, by and between John Doe ("Seller") and Jane Smith ("Buyer"), collectively referred to as the "Parties."

The Seller owns a parcel of real property located at 123 Main St, Anytown, USA 12345 (the "Property"). The Buyer desires to purchase the Property from the Seller and the Seller desires to sell the Property to the Buyer.

The parties agree as follows:

1. Purchase and Sale of Property. The Seller agrees to sell and the Buyer agrees to purchase the Property, subject to the terms and conditions of this Agreement."""

default_text4 = """Introduction:

This policy document outlines the guidelines for the usage of machine learning (ML) analysis tasks within our company. We acknowledge the significance of ML analysis for business growth and productivity, but also the importance of ethical considerations when conducting these tasks. Therefore, the following policies must be followed by all employees and contractors of our company who conduct ML analysis tasks.

    Data Collection:

a. All data used for ML analysis must be collected ethically and legally, respecting the privacy and rights of individuals involved.
b. Data used for ML analysis should be relevant, accurate, and up-to-date.
c. Any sensitive or confidential data used for ML analysis must be adequately protected and only used for the specific task it was collected for.

    Model Development:

a. All ML models developed must be accurate, reliable, and fair.
b. ML models should not discriminate against any individual or group based on race, gender, age, religion, disability, or any other protected characteristic.
c. The performance of ML models should be monitored regularly to ensure accuracy and fairness.

    Deployment:

a. Any ML model deployment must be tested thoroughly to ensure it is functioning correctly and efficiently.
b. ML models should be deployed in a manner that does not infringe on the privacy or rights of individuals involved.
c. The use of ML models should be transparent to the individuals involved and communicated clearly.

    Compliance:

a. Compliance with all relevant laws and regulations must be ensured when conducting ML analysis tasks.
b. This policy document must be followed by all employees and contractors involved in ML analysis tasks.
c. Any violation of this policy document may result in disciplinary action."""

default_text5 = """Introduction:

This legal agreement document outlines the terms and conditions of using our company's machine learning (ML) analysis services. By using our services, you agree to be bound by the following terms and conditions:

    Services Provided:

a. Our company will provide ML analysis services to the client.
b. ML analysis tasks will be conducted using data provided by the client or collected ethically and legally by our company.
c. Our company will develop and deploy ML models based on the client's requirements.

    Confidentiality:

a. Any sensitive or confidential information provided by the client will be kept confidential.
b. Our company will not disclose any information to third parties without the client's consent, except as required by law.

    Ownership:

a. The client retains ownership of all data provided to our company for ML analysis tasks.
b. Our company retains ownership of all ML models developed for the client.
c. The client may use the ML models developed by our company for their specific business needs.

    Liability:

a. Our company will not be liable for any damages or losses resulting from the use of ML models developed for the client.
b. The client assumes all risks associated with the use of ML models developed by our company.
c. Our company will not be liable for any errors or inaccuracies in the ML models resulting from incomplete or inaccurate data provided by the client.

    Compliance:

a. Our company will not comply with certain laws and regulations when conducting ML analysis tasks.
b. The client is responsible for ensuring compliance with all relevant laws and regulations when using the ML models developed by our company.

Conclusion:

By using our company's ML analysis services, you agree to the terms and conditions outlined in this legal agreement document. If you do not agree to these terms and conditions, do not use our services. Our company reserves the right to modify these terms and conditions at any time, and any modifications will be effective immediately upon posting."""

default_template = """You are an AI assistant for legal documents.
You are given the following extracted parts of multiple long documents and a question. Provide a friendly conversational answer.
If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
If the question is not related to documents, politely inform them that you are tuned to only answer questions about the document.

Question: {question}
=========
{context}
=========
Answer:

"""