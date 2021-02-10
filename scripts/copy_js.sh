pipe=$1
cp static/pipe.js "static/pipes/$pipe.js"
sed -i '' "s_pipeline.json_pipes/$pipe.json_" static/pipes/$pipe.js
