require 'csv'
require 'json'
require 'open-uri'

def blank?(el)
  el.nil? || el.strip == ''
end

def present?(el)
  !blank?(el)
end

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS-e9fdKtTmkC6ig7SNTDTLJ6ndX427IWNqD3NDe6nv-GC6ka-VTEa-UVlcnquWMCFjgCx6shk5UNUO/pub?gid=0&single=true&output=csv'
csv = CSV.parse(open(url, encoding: 'utf-8'), headers: true)

json = {
    nest: {},
    monsters: {}
}

hash = Hash.new { |h, k| h[k] = [] }

csv.each do |row|
  nest, monsters = row['nest'], row['monsters'].split('、')
  json[:nest][nest] = monsters
  monsters.each do |name|
    hash[name] << nest
  end
end
json[:monsters] = hash

file = File.open('sr-nest-data-staging.json', 'wb')
file.write(json.to_json)
file.close
