## Problem Statement:
In regions where rapid new urban development emerges, home prices tend to become less affordable in the initial phase of the development. This phenomena occurs in many U.S. and Canadian cities such as San Francisco, Denver, and Vancouver, where the residents' income level does not keep up with the fast increase in home prices.

Home affordability ratio is defined as the home price and median annual income ratio. "Historically a house in the US cost around 3 to 4 times the median annual income. During the housing bubble of 2007 the ratio surpassed 5 - in other words, the median price for a single family home in the United States cost more than 5 times the US median annual household income"(reference). In recent years, many U.S. and Canadian neighborhoods have become unaffordable for the residents.

In my project, I will explore whether commercial activities in a given neighborhood can be an indicator for the affordability of home prices. In particular, I will explore which types of business might be the best indicator of the neighborhood's affordability level. This approch has the advantage of lower costs than the traditional method based on census information. It can also serve as an early indicator used by a municipality: if certain patterns of business activities emerges, the problem of a neighborhood becomes unaffordable might fellow.

I will use the Google Places API to gather data about neighborhood businesses, such as types, opening hours, price level etc. To calculate Home affordability ratio, I will scrap home prices data from Zillow, divided by the median income collected from US Cecus Bereau(good and cheap) (or buy the data from incomebyzipcode.com(Fast and Good).

I will use unsupervised model during the EDA process to explore patterns of commercial activities. I will develop supervised regression models to predict affordability.

My project will be develped in 4 phases:

Phase 1: Case study of NYC: develop models using NYC data
Phase 2: Test if model is transferable for other urban areas, such as L.A. or Toronto
Phase 3: Generlization: Test model can be generized and used in any given urban areas.
Phase 4: Web interface: Develop a simple web interface so a client can imput informations, and receive predictions.