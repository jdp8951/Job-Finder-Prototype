const  express=require("express");
const app=express();
const path=require("path");


app.set("view engine","ejs");
app.set("views",path.join(__dirname,"views"));
app.use(express.urlencoded({extended:true}));
app.use(express.static(path.join(__dirname, "public")));

app.get("/",(req,res)=>{
   res.render("home");
});

app.get("/jobs",(req,res)=>{
  res.render("jobs");
});

app.get("/login", (req, res) => {
    res.render("login");
  });
  
app.get("/signup", (req, res) => {
    res.render("signup");
  });

  app.get("/about", (req, res) => {
    res.render("about");
  });

app.listen(8080, ()=>{
    console.log("server is listening on port 8080");
});
