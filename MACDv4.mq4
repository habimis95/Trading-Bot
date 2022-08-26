//Variable Declaration
extern string starttime = "10:00";
extern string endtime = "18:00";
string currentTime;
bool timecheck = false;
double lots= 0.01;
extern double takeprofit = 60;
extern double stoploss = 45;
int loaiLenh = OP_BUY;
int  magic =999;
string sym;
string Com;
string vol = "Lot Size";
string symBuy[] = {"EURGBP", "USDJPY", "EURJPY", "NZDJPY", "GBPUSD", "EURUSD"};
string symSell[] = {"CHFJPY", "USDCHF", "NZDUSD", "AUDCAD"};

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   sym=Symbol() ;
   
//---
   return(INIT_SUCCEEDED);
  }  
  
  
  
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
 
   
   
  }
  
  
  
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {//get the local time
   datetime time = TimeGMT();
   //format the time and create a string
   currentTime = TimeToString(time, TIME_MINUTES);
   if(checkTime() == false){return;}
   if(demsolenh(sym)>0){return;}
  
   
  // Conditions to send order 
   double currentMACD = iMACD(NULL, 0, 12, 26, 9, PRICE_CLOSE, MODE_MAIN, 0);
   double previousMACD = iMACD(NULL, 0, 12, 26, 9, PRICE_CLOSE, MODE_MAIN, 1);
   double previous1MACD = iMACD(NULL, 0, 12, 26, 9, PRICE_CLOSE, MODE_MAIN, 2);
   
   if(previousMACD>0 && previous1MACD<0 && currentMACD>0 && CheckBuySymbol(Symbol())){loaiLenh=OP_BUY;}
   else if(previousMACD<0 && previous1MACD>0 && currentMACD<0 && CheckBuySymbol(Symbol())){loaiLenh=OP_SELL;}else return;
    
      if(IsNewCandle() && CheckMoneyForTrade(Symbol(),lots,loaiLenh)
                       && CheckVolumeValue(lots,vol)
                       && IsNewOrderAllowed())
    {
   vaoLenh(sym,loaiLenh,lots,0,stoploss,takeprofit,magic,Com);
   Comment("Trading time:", timecheck,"\n",
           "Current time:", currentTime,"\n",
           "Start time:", starttime,"\n",
           "End time:", endtime,"\n",
           "MACD Value at Buy:", currentMACD,"\n");
  }
}
//+------------------------------------------------------------------+

//Count the number of orders
int demsolenh(string captiencandem)
{
   int dem;
   for(int i = OrdersTotal()-1 ; i>=0; i--)
   {
    if(OrderSelect(i, SELECT_BY_POS,MODE_TRADES)==False)  {continue;}
    if(OrderSymbol() != captiencandem){continue;}
    if(OrderMagicNumber()!= magic){continue;}
        dem ++;// dem dc 1 lenh
   }
return(dem);
}

void   vaoLenh(string symm, int typee, double lott, double pricee, double slpip,double tppip,int magicc, string comm )
{
   if(lott ==0){return;}
   int normallotunit  ;
   if(MarketInfo(symm, MODE_MINLOT)== 0.01){normallotunit = 2;}
   if(MarketInfo(symm, MODE_MINLOT)== 0.1){normallotunit = 1;}
   if(MarketInfo(symm, MODE_MINLOT)== 0.001){normallotunit = 3;}
   lott = NormalizeDouble(lott, normallotunit );
   //---------------------------
   double slprice, tpprice; color mau;
   if(typee== OP_BUY)
       {
         pricee = MarketInfo(symm,MODE_ASK);
         slprice = pricee - slpip*10*MarketInfo(symm ,MODE_POINT);
         tpprice = pricee + tppip*10*MarketInfo(symm ,MODE_POINT);
         mau = clrBlue;
       }

   if(typee== OP_SELL)
       {
         pricee = MarketInfo(symm,MODE_BID);
         slprice = pricee + slpip*10*MarketInfo(symm ,MODE_POINT);
         tpprice = pricee - tppip*10*MarketInfo(symm ,MODE_POINT);
         mau = clrRed;
       }
   pricee = NormalizeDouble(pricee,MarketInfo(symm , MODE_DIGITS));
   slprice = NormalizeDouble(slprice,MarketInfo(symm , MODE_DIGITS));
   tpprice = NormalizeDouble(tpprice,MarketInfo(symm , MODE_DIGITS));
  //-----gui lenh
   double thanhcong = OrderSend(symm,typee,lott,pricee,20,0,0,comm,magicc,0,mau);
  // ----- CHINH SL TP
  bool sucess =false; int dem;
  if(thanhcong >0 && slprice !=0 && tpprice!=0 )
      {
         while ( sucess == false && dem<20)
         {  sucess =  OrderModify(thanhcong,pricee,slprice,tpprice,0,clrNONE);
          dem++; Sleep(50);
         }
      int error = GetLastError();
      if(error !=0 && error !=1){ Print("bi loi: "+ error);}
      }
}

// Check time:
bool checkTime()
{ 
  
 
   if(StringSubstr(currentTime,0,5)== starttime)
      {timecheck=true;}
   else if(StringSubstr(currentTime,0,5)== endtime)
      {timecheck=false;} 
   else return timecheck;
   return false;
}
//Check Buy Symbol
bool CheckBuySymbol(string symmm)
   {  
      bool check = false;
      for(int i=0; i<ArraySize(symBuy);i++)
         {
            if(StringFind(symBuy[i],Symbol()) != -1)
               {
                  return true;
                  break;
               }
            else return false;
         }
       if(check==true){return true;}
       else return false;
   }
//Check Sell Symbol
bool CheckSellSymbol(string symmm)
   {  
      bool check = false;
      for(int i=0; i<ArraySize(symSell);i++)
         {
            if(StringFind(symSell[i],Symbol()) != -1)
            {
               return check = true;
               break;
            }
           else return false;
         }
        if(check==true){return true;}
        else return false;
   }
   
//Check is there any OrderSends per candle?
bool IsNewCandle()
{
   static  datetime saved_candle_time;
   if(Time[0] == saved_candle_time)
      return false;
   else
      saved_candle_time = Time[0];
   return true;
}



//CheckVolumneValue
bool CheckVolumeValue(double volume,string &description)

  {

//--- minimal allowed volume for trade operations

   double min_volume=SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_MIN);

   if(volume<min_volume)

     {

      description=StringFormat("Volume is less than the minimal allowed SYMBOL_VOLUME_MIN=%.2f",min_volume);

      return(false);

     }



//--- maximal allowed volume of trade operations

   double max_volume=SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_MAX);

   if(volume>max_volume)

     {

      description=StringFormat("Volume is greater than the maximal allowed SYMBOL_VOLUME_MAX=%.2f",max_volume);

      return(false);

     }



//--- get minimal step of volume changing

   double volume_step=SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_STEP);



   int ratio=(int)MathRound(volume/volume_step);

   if(MathAbs(ratio*volume_step-volume)>0.0000001)

     {

      description=StringFormat("Volume is not a multiple of the minimal step SYMBOL_VOLUME_STEP=%.2f, the closest correct volume is %.2f",

                               volume_step,ratio*volume_step);

      return(false);

     }

   description="Correct volume value";

   return(true);

  }
  
//Check Money for Trade
 bool CheckMoneyForTrade(string symb, double lotss,int type)

  {

   double free_margin=AccountFreeMarginCheck(symb,type, lotss);

   //-- if there is not enough money

   if(free_margin<0)

     {

      string oper=(type==OP_BUY)? "Buy":"Sell";

      Print("Not enough money for ", oper," ",lots, " ", symb, " Error code=",GetLastError());

      return(false);

     }

   //--- checking successful

   return(true);

  }
bool IsNewOrderAllowed()
  {
//--- get the number of pending orders allowed on the account
   int max_allowed_orders=(int)AccountInfoInteger(ACCOUNT_LIMIT_ORDERS);

//--- if there is no limitation, return true; you can send an order
   if(max_allowed_orders==0) return(true);

//--- if we passed to this line, then there is a limitation; find out how many orders are already placed
   int orders=OrdersTotal();

//--- return the result of comparing
   return(orders<max_allowed_orders);
  }

