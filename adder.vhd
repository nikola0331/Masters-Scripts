library IEEE;
use IEEE.std_logic_1164.all;  
use IEEE.numeric_std.all;
--use std.textio.all;
Library UNISIM;
use UNISIM.vcomponents.all;

--library std.textio;
use std.textio.all;
use IEEE.std_logic_textio.all;

Library UNIMACRO;
use UNIMACRO.vcomponents.all;

ENTITY adder IS

PORT (
    CLK: in std_logic;
    CE: in std_logic;
    RST: in std_logic;
    nr1, nr2: in std_logic_vector(7 downto 0);   
    --output1, output3: out std_logic_vector(17 downto 0);
    --output2 : out std_logic_vector(7 downto 0);
    --carryI: in std_logic;
    sum1, sum2: inout std_logic_vector(15 downto 0); -- sum1, 
    carryO: out std_logic
    --addsub: in std_logic
);
END ENTITY adder;

architecture test of adder is -- where declarations are placed

    signal CARRYOUT, CARRYIN: std_logic; -- 1-bit carry-out output signal
    signal RESULT :  std_logic_vector(15 downto 0);     -- Add/sub result output, width defined by WIDTH generic
    signal A :  std_logic_vector(7 downto 0);          -- Input A bus, width defined by WIDTH generic
    signal A1 :  std_logic_vector(15 downto 0);  
    signal ADD_SUB :  std_logic;  -- 1-bit add/sub input, high selects add, low selects subtract
    signal B :  std_logic_vector(7 downto 0);   -- Input B bus, width defined by WIDTH generic
    signal B1 :  std_logic_vector(15 downto 0);
    signal P :  std_logic_vector(15 downto 0);
    signal temp1 : std_logic_vector(15 downto 0) := (others => '0'); -- answer of multiplication
    signal count :  std_logic_vector (7 downto 0):= "00000001";
    signal addsub : std_logic := '1';
    signal carryI : std_logic := '0';

   

begin  

    
    ADDSUB_MACRO_inst : ADDSUB_MACRO
       generic map (
          DEVICE => "7SERIES", -- Target Device: "VIRTEX5", "7SERIES", "SPARTAN6" 
          LATENCY => 1,        -- Desired clock cycle latency, 0-2
          WIDTH => 16)         -- Input / Output bus width, 1-48
       port map (
          CARRYOUT => CARRYOUT, -- 1-bit carry-out output signal
          RESULT => RESULT,     -- Add/sub result output, width defined by WIDTH generic
          A => A1,               -- Input A bus, width defined by WIDTH generic
          ADD_SUB => ADD_SUB,   -- 1-bit add/sub input, high selects add, low selects subtract
          B => B1,               -- Input B bus, width defined by WIDTH generic
          CARRYIN => CARRYIN,   -- 1-bit carry-in input
          CE => CE,             -- 1-bit clock enable input
          CLK =>CLK,           -- 1-bit clock input
          RST => RST            -- 1-bit active high synchronous reset
       );
       
       MULT_MACRO_inst : MULT_MACRO
       generic map (
          DEVICE => "7SERIES",    -- Target Device: "VIRTEX5", "7SERIES", "SPARTAN6" 
          LATENCY => 0,           -- Desired clock cycle latency, 0-4
          WIDTH_A => 8,          -- Multiplier A-input bus width, 1-25 
          WIDTH_B => 8)          -- Multiplier B-input bus width, 1-18
       port map (
          P => P,     -- Multiplier ouput bus, width determined by WIDTH_P generic 
          A => A,     -- Multiplier input A bus, width determined by WIDTH_A generic 
          B => B,     -- Multiplier input B bus, width determined by WIDTH_B generic 
          CE => CE,   -- 1-bit active high input clock enable
          CLK => CLK, -- 1-bit positive edge clock input
          RST => RST  -- 1-bit input active high reset
       );
       
    multiply : process (CLK, nr1, nr2)
    begin
    if CLK'event and CLK = '1' then
        A <= nr1;
        B <= nr2;
        --output1 <= P;
        temp1 <= P;           
     end if;         
    end process multiply;
          

    
        average : process (CLK, RST)
  variable temp : std_logic_vector(15 downto 0) := (others => '0');
  variable sum1_1, sum2_1 : std_logic_vector(15 downto 0)  := (others => '0');
    begin
        sum1_1 := sum1;
       if RST'event and RST = '1' then
            
                --sum1_1 := (others => '0');
                count <= "00000001";
                --sum2_1 := (others => '0');
                temp := (others => '0'); 
            
        end if; -- RESET ELSE   
           
        if CLK'event and CLK = '1' then
        if temp1 /= P then    
           if count < "10000000" then
        	       count <= count(6 downto 0) & '0'; -- logic shift left to double nr
        	       -- add nr to sum
        	        A1 <= temp1; --comes from multiplier
                    B1 <= sum1_1; --"000000000000000010"; -- accumulated value up to now
                    ADD_SUB <= addsub;
                    CARRYIN <=  carryI;
            	    carryO <= CARRYOUT;
            	    temp := RESULT;
                    
                else -- if reached 8 additions
                     count <= "00000001";-- reset to 1
                     
                     if temp > "0000000000000000" then
                          sum2_1 := std_logic_vector("000" & temp(15 downto 3)); -- calculate the average of the past 8
					 elsif temp < "0000000000000000" then
					      sum2_1 := std_logic_vector("1000" & temp(14 downto 3)); -- if it's negative
					 else sum2_1 := (others => '0');
					 end if;
					 sum1_1 := (others => '0');
					 --temp3 <= (others => '0'); 
					  temp := (others => '0'); 
                end if; -- COUNT <= 128
        end if; -- tmp /= P, multiplication done     
        end if; -- clk event 
        
        sum2 <= sum2_1;
        sum1 <= temp;    
    end process average;
    --temp2 <= temp1;
    --sum <= avg;
    --temp2 <= P;
    
    --output1 <= temp1;
    --output2 <= count;
    -- temp3 <= temp1;
    --output3 <= sum1;
end architecture test;