#!/bin/bash

# Tamil Calendar API - Push to GitHub Script
# Run this AFTER creating the repository on GitHub

echo "Tamil Calendar API - GitHub Push Script"
echo "========================================"
echo ""
echo "IMPORTANT: Before running this script:"
echo "1. Go to: https://github.com/organizations/wearepixwell/repositories/new"
echo "2. Create a repository named: tamil-calendar-api"
echo "3. Set it to Public"
echo "4. DO NOT initialize with README"
echo ""
read -p "Have you created the repository on GitHub? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Please create the repository first, then run this script again."
    exit 1
fi

echo ""
echo "Setting up git remote..."
git remote add origin https://github.com/wearepixwell/tamil-calendar-api.git

echo "Renaming branch to main..."
git branch -M main

echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Done! Your Tamil Calendar API is now on GitHub!"
echo "Visit: https://github.com/wearepixwell/tamil-calendar-api"
echo ""
echo "Next step: Deploy to Railway"
echo "1. Go to: https://railway.app"
echo "2. Click 'New Project'"
echo "3. Select 'Deploy from GitHub repo'"
echo "4. Choose 'tamil-calendar-api'"
echo "5. Railway will automatically deploy!"
