# autopkg

These are some Autopkg recipes that I came up with because I thought I could maybe make things work better, or more in line with my requirements, than whatever I happened to have found at that point.  Also because I like a challenge!

## Office recipes

In September 2018, Microsoft announced the release of Office 2019.  Up until that point, Office 365 and Office 2016 used the same installer.  Following the release, Office 365 became feature-compatible with Office 2019, thereby separating the 2016 installer.
This seems to have caused some confusion for Autopkg users, with different recipes claiming to download 2016 installers, but actually providing the 365 version, or using 365 version numbers.  I wanted to create recipes that made use of the informatiom provided by Paul Bowden at https://macadmins.software, allowed the downloading of either the 2016 or 365 installers, and used the correct version numbers.

There are two recipe families: **Office** and **OfficeExtras**.
The **Office** recipes cover the licensed Office suite products: the complete suite installer, and the standalone versions of Word, Excel, Powerpoint and Outlook.  They share a common version numbering scheme.
The **OfficeExtras** recipes cover the ancillary products associated with Office.  Whilst OneNote, OneDrive, and MAU are also included in the Office installer, they do not require licensing, and they use different version numbering.  Skype for Business, Teams, the InTune Company Portal, and Remote Desktop are completely separate products.

As is best practice, you should create one or more local overrides of these recipes.  If you want to download more than one product covered by a single recipe, then you will need to create an override for each one.
